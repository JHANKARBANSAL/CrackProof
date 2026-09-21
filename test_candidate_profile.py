"""Resume/profile tests use synthetic PDFs, fake AI, and temporary databases."""
import io
import unittest
from unittest.mock import patch

from pydantic import ValidationError
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject

import candidate_profile as profiles
import database
import test_web


def resume_pdf(text="Python SQL developer. Built a library application using Python and SQL.", pages=1, password=None):
    writer = PdfWriter()
    for _ in range(pages):
        page = writer.add_blank_page(width=612, height=792)
        font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})
        page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
        stream = DecodedStreamObject()
        stream.set_data(f"BT /F1 12 Tf 50 700 Td ({text}) Tj ET".encode())
        page[NameObject("/Contents")] = stream
    if password:
        writer.encrypt(password)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


class ResumeTests(unittest.TestCase):
    def test_reads_real_pdf_text(self):
        self.assertIn("Python SQL developer", profiles.read_resume(resume_pdf()))

    def test_rejects_unsupported_pdfs(self):
        for data in [b"hello", b"%PDF-invalid", resume_pdf(text=""), resume_pdf(pages=11), resume_pdf(password="secret"), b"%PDF-" + b"x" * profiles.MAX_PDF_BYTES]:
            with self.subTest(size=len(data)), self.assertRaises(ValueError):
                profiles.read_resume(data)

    def test_profile_validation_and_deduplication(self):
        data = {"target_role": " Backend Developer ", "experience_level": "Fresher", "skills": [" Python ", "python", "SQL"]}
        profile = profiles.CandidateProfile.model_validate(data)
        self.assertEqual(profile.skills, ["Python", "SQL"])
        self.assertEqual(profile.target_role, "Backend Developer")
        for changes in [{"skills": []}, {"skills": [" "]}, {"target_role": " "}, {"experience_level": "anything"}, {"owner_key": "user:2"}]:
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                profiles.CandidateProfile.model_validate({**data, **changes})
        with self.assertRaises(ValidationError):
            profiles.CandidateProfile.model_validate({"target_role": "Developer", "experience_level": "Fresher"})


class ProfileAPITests(unittest.TestCase):
    setUpClass = classmethod(test_web.WebRegressionTests.setUpClass.__func__)
    setUp = test_web.WebRegressionTests.setUp
    login = test_web.WebRegressionTests.login

    def test_short_job_description_gives_guidance_without_ai(self):
        with patch.object(profiles, "ask_llm") as ai:
            response = self.client.post("/api/profile/job-description", json={"target_role": "Backend Developer", "job_description": "Python role"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["review"]["assessment"], "needs_detail")
        ai.assert_not_called()

    def test_job_description_relevance_and_exact_evidence(self):
        description = "Build Python APIs using PostgreSQL, write automated tests and collaborate with frontend developers on backend services."
        review = profiles.JobDescriptionReview(assessment="useful", summary="Relevant backend responsibilities.", relevant_skills=["Python", "PostgreSQL"], focus_areas=["API design"], missing_details=[], evidence=["Build Python APIs", "Fabricated requirement"])
        with patch.object(profiles, "ask_llm", return_value=review):
            response = self.client.post("/api/profile/job-description", json={"target_role": "Backend Developer", "job_description": description})
        self.assertEqual(response.json["review"]["evidence"], ["Build Python APIs"])
        self.assertIsNone(self.client.get("/api/profile").json["profile"])

    def test_invalid_job_description_and_ai_failure(self):
        for payload in [{}, {"target_role": " ", "job_description": "role"}, {"target_role": "Backend", "job_description": "x" * 8001}]:
            self.assertEqual(self.client.post("/api/profile/job-description", json=payload).status_code, 400)
        with patch.object(profiles, "ask_llm", return_value=None):
            response = self.client.post("/api/profile/job-description", json={"target_role": "Backend Developer", "job_description": "Build reliable Python APIs with databases, automated tests, logging, monitoring and deployment responsibilities."})
        self.assertEqual(response.status_code, 502)

    def test_unrelated_description_does_not_suggest_unrelated_interview(self):
        review = profiles.JobDescriptionReview(assessment="role_mismatch", summary="This is a chef role.", relevant_skills=["Baking"], focus_areas=["Bread recipes"], missing_details=["Salary"], evidence=[])
        with patch.object(profiles, "ask_llm", return_value=review):
            result = profiles.review_job_description("Backend Developer", "Prepare bread and cakes, maintain the kitchen and manage ingredient stock for our restaurant.")
        self.assertEqual(result.focus_areas, [])
        self.assertIn("Backend Developer", result.missing_details[0])

    def test_profile_save_reload_and_owner_isolation(self):
        payload = {"target_role": "Backend Developer", "experience_level": "Fresher", "skills": ["Python"]}
        self.assertTrue(self.client.post("/api/profile", json=payload).json["ok"])
        self.assertEqual(self.client.get("/api/profile").json["profile"]["skills"], ["Python"])
        self.assertIsNone(self.other.get("/api/profile").json["profile"])
        user_id = self.login(self.client, "profile@example.com")
        self.assertIsNone(self.client.get("/api/profile").json["profile"])
        self.client.post("/api/profile", json=payload)
        database.delete_account(user_id)
        self.assertIsNone(database.load_profile("user:" + str(user_id)))

    def test_invalid_profile_does_not_replace_saved(self):
        payload = {"target_role": "Developer", "experience_level": "Fresher", "skills": ["SQL"]}
        self.client.post("/api/profile", json=payload)
        self.assertEqual(self.client.post("/api/profile", json={**payload, "skills": []}).status_code, 400)
        self.assertEqual(self.client.get("/api/profile").json["profile"]["skills"], ["SQL"])

    def test_resume_parse_is_preview_only(self):
        with patch.object(profiles, "ask_llm", return_value=profiles.ResumeDetails(skills=["Python"])) as ai:
            response = self.client.post("/api/resume/parse", data={"resume": (io.BytesIO(resume_pdf()), "resume.pdf")})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["details"]["skills"], ["Python"])
        self.assertIsNone(self.client.get("/api/profile").json["profile"])
        self.assertIn("Python SQL developer", ai.call_args.args[0])

    def test_bad_uploads_do_not_call_ai_and_failure_is_retryable(self):
        with patch.object(profiles, "ask_llm", return_value=None) as ai:
            for filename, data in [("resume.txt", b"text"), ("resume.pdf", b"fake")]:
                response = self.client.post("/api/resume/parse", data={"resume": (io.BytesIO(data), filename)})
                self.assertEqual(response.status_code, 400)
            ai.assert_not_called()
            response = self.client.post("/api/resume/parse", data={"resume": (io.BytesIO(resume_pdf()), "resume.pdf")})
            self.assertEqual(response.status_code, 502)


if __name__ == "__main__":
    unittest.main()
