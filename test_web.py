"""Offline regression tests. Uses temporary databases and mocked AI responses."""

import importlib
import io
import os
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch, Mock

import database
import interview_session
from evaluator import AnswerEvaluation


EVALUATION = AnswerEvaluation(
    verdict="PARTIALLY_CORRECT", correctness_score=6, depth_score=4,
    correct_points=["Definition is correct"], missing_core_concepts=["Explain the trade-off"],
    deeper_concepts_to_probe=[], misconceptions=[], citations=[],
    evidence=[{"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED",
               "evidence_from_answer": "Definition"}], reasoning="Application is missing.")


class WebRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Importing server initializes tables, so isolate that import as well.
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(database, "DATABASE_URL", ""), patch.object(database, "DB_FILE", os.path.join(directory, "import.db")):
                cls.server = importlib.import_module("server")
        cls.server.app.config.update(TESTING=True, SECRET_KEY="test-only-key")

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        replacements = [
            patch.object(database, "DATABASE_URL", ""),
            patch.object(database, "DB_FILE", os.path.join(self.directory.name, "test.db")),
            patch.object(interview_session, "RECORDINGS_DIR", self.directory.name),
            patch.object(self.server, "RECORDINGS_DIR", self.directory.name),
            patch.object(interview_session, "generate_first_question", return_value="Explain an interface."),
            patch.object(interview_session, "generate_followup", return_value="Give an example."),
            patch.object(interview_session, "generate_continuation_question", return_value="Explain inheritance."),
            patch.object(interview_session, "get_reference", return_value=("Reference", [])),
            patch.object(interview_session, "evaluate_answer", return_value=EVALUATION),
            patch("reporting.generate_final_assessment", return_value=None),
        ]
        for replacement in replacements:
            replacement.start()
            self.addCleanup(replacement.stop)
        database.setup()
        self.client = self.server.app.test_client()
        self.other = self.server.app.test_client()

    def start(self, client=None):
        response = (client or self.client).post("/api/start", json={"topic": "Java"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["ok"])
        return response.json["interview_id"]

    def evaluate(self, interview_id, question_number=1, client=None):
        return (client or self.client).post("/api/evaluate", json={
            "interview_id": interview_id, "question_number": question_number,
            "transcript": "An interface defines a contract."})

    def login(self, client, email):
        with patch.object(database, "validate_email_address", return_value=(True, None)):
            response = client.post("/api/signup", json={"email": email, "password": "test-password", "name": "Test"})
        self.assertTrue(response.json["ok"])
        return response.json["user"]["id"]

    def test_setup_is_repeatable(self):
        database.setup()
        self.assertTrue(self.client.get("/api/me").json["ok"])

    def test_ids_are_unique_and_unknown_sessions_do_not_regenerate(self):
        first, second = self.start(), self.start()
        self.assertNotEqual(first, second)
        with patch.object(interview_session, "generate_first_question") as generate:
            self.assertEqual(self.evaluate("unknown").status_code, 404)
            generate.assert_not_called()

    def test_state_survives_a_new_client_with_the_same_cookie(self):
        interview_id = self.start()
        self.evaluate(interview_id)
        fresh = self.server.app.test_client()
        fresh.set_cookie("session", self.client.get_cookie("session").value)
        with patch.object(interview_session, "generate_first_question") as generate:
            result = fresh.post("/api/next", json={"interview_id": interview_id, "question_number": 1})
            self.assertEqual(result.json["question_number"], 2)
            generate.assert_not_called()
        self.assertEqual(len(fresh.get("/api/history/subject/Java").json["questions"]), 1)

    def test_duplicate_evaluation_does_not_count_twice(self):
        interview_id = self.start()
        self.assertTrue(self.evaluate(interview_id).json["ok"])
        with patch.object(interview_session, "evaluate_answer") as evaluate:
            self.assertTrue(self.evaluate(interview_id).json["ok"])
            evaluate.assert_not_called()
        self.assertEqual(self.client.get("/api/history").json["interviews"][0]["questions_answered"], 1)

    def test_stale_answer_and_next_do_not_skip_questions(self):
        interview_id = self.start()
        self.evaluate(interview_id)
        body = {"interview_id": interview_id, "question_number": 1}
        self.assertEqual(self.client.post("/api/next", json=body).json["question_number"], 2)
        self.assertEqual(self.client.post("/api/next", json=body).json["question_number"], 2)
        self.assertEqual(self.evaluate(interview_id).status_code, 409)

    def test_guests_cannot_read_or_change_other_guests_interviews(self):
        interview_id = self.start()
        self.evaluate(interview_id)
        self.assertEqual(self.evaluate(interview_id, client=self.other).status_code, 404)
        self.assertEqual(self.other.get("/api/interview/" + interview_id).status_code, 404)
        history = self.other.get("/api/history/subject/Java?guest_ids=" + interview_id).json
        self.assertEqual(history["questions"], [])
        topics = self.other.get("/api/history/topics?guest_ids=" + interview_id).json["topics"]
        self.assertEqual(sum(t["attempts"] for t in topics), 0)

    def test_account_ownership_and_logout(self):
        self.login(self.client, "first@example.test")
        self.login(self.other, "second@example.test")
        interview_id = self.start()
        self.evaluate(interview_id)
        self.assertEqual(self.other.get("/api/interview/" + interview_id).status_code, 404)
        self.assertEqual(self.evaluate(interview_id, client=self.other).status_code, 404)
        self.client.post("/api/logout", json={})
        self.assertIsNone(self.client.get("/api/me").json["user"])
        self.assertEqual(self.client.get("/api/interview/" + interview_id).status_code, 404)

    def test_final_report_preserves_turns_and_can_be_read_without_ai(self):
        self.login(self.client, "first@example.test")
        interview_id = self.start()
        self.evaluate(interview_id)
        self.assertTrue(self.client.post("/api/report", json={"interview_id": interview_id}).json["ok"])
        with patch.object(interview_session, "build_report") as build:
            saved = self.client.get("/api/interview/" + interview_id).json["interview"]["report"]
            self.assertEqual(len(saved["turns"]), 1)
            self.assertEqual(saved["metrics"]["questions_answered"], 1)
            self.client.post("/api/report", json={"interview_id": interview_id})
            build.assert_not_called()
        self.assertEqual(len(self.client.get("/api/history/subject/Java").json["questions"]), 1)

    def test_empty_report_does_not_finish_interview(self):
        interview_id = self.start()
        self.assertFalse(self.client.post("/api/report", json={"interview_id": interview_id}).json["ok"])
        self.assertTrue(self.evaluate(interview_id).json["ok"])

    def test_ai_failures_keep_current_question_and_allow_retry(self):
        interview_id = self.start()
        with patch.object(interview_session, "evaluate_answer", return_value=None):
            self.assertFalse(self.evaluate(interview_id).json["ok"])
        self.assertTrue(self.evaluate(interview_id).json["ok"])
        with patch.object(interview_session, "generate_followup", return_value=None):
            self.assertFalse(self.client.post("/api/next", json={"interview_id": interview_id}).json["ok"])
        self.assertEqual(self.client.post("/api/next", json={"interview_id": interview_id}).json["question_number"], 2)

    def test_quality_failure_is_not_overridden_by_nonempty_transcript(self):
        interview_id = self.start()
        with patch.object(interview_session, "transcribe_audio", return_value=("noise", "Speech is unclear")):
            result = self.client.post("/api/transcribe", data={
                "interview_id": interview_id, "audio": (io.BytesIO(b"test"), "answer.webm")})
        self.assertFalse(result.json["ok"])
        self.assertEqual(result.json["message"], "Speech is unclear")

    def test_stale_revision_cannot_overwrite_saved_answer(self):
        interview_id = self.start()
        with self.client.session_transaction() as cookie:
            owner = "guest:" + cookie["guest_id"]
        state, revision = database.load_session(interview_id, owner)
        self.evaluate(interview_id)
        self.assertFalse(database.save_session(interview_id, owner, state, revision))
        self.assertEqual(len(database.load_session(interview_id, owner)[0]["history"]), 1)

    def test_delete_removes_state_feedback_and_history(self):
        user_id = self.login(self.client, "first@example.test")
        interview_id = self.start()
        self.evaluate(interview_id)
        self.client.post("/api/feedback", json={"interview_id": interview_id, "question_number": 1, "was_fair": True})
        self.assertTrue(self.client.post("/api/interview/" + interview_id + "/delete").json["ok"])
        self.assertIsNone(database.load_session(interview_id, "user:" + str(user_id)))
        self.assertEqual(self.client.get("/api/history").json["interviews"], [])
        self.assertEqual(database.feedback_summary()["total"], 0)

    def test_feedback_requires_ownership_and_boolean(self):
        interview_id = self.start()
        self.evaluate(interview_id)
        body = {"interview_id": interview_id, "question_number": 1, "was_fair": True}
        self.assertEqual(self.other.post("/api/feedback", json=body).status_code, 404)
        body["was_fair"] = "false"
        self.assertEqual(self.client.post("/api/feedback", json=body).status_code, 400)

    def test_five_question_batch_cannot_overrun(self):
        interview_id = self.start()
        for number in range(1, 6):
            self.assertTrue(self.evaluate(interview_id, number).json["ok"])
            if number < 5:
                self.client.post("/api/next", json={"interview_id": interview_id})
        self.assertFalse(self.client.post("/api/next", json={"interview_id": interview_id}).json["ok"])
        self.assertTrue(self.client.post("/api/report", json={"interview_id": interview_id}).json["ok"])

    def test_concurrent_evaluations_only_commit_one_answer(self):
        interview_id = self.start()
        cookie = self.client.get_cookie("session").value
        barrier = Barrier(2)

        def evaluate_once():
            client = self.server.app.test_client()
            client.set_cookie("session", cookie)
            return self.evaluate(interview_id, client=client).status_code

        def delayed_evaluation(**kwargs):
            barrier.wait(timeout=5)
            return EVALUATION

        with patch.object(interview_session, "evaluate_answer", side_effect=delayed_evaluation):
            with ThreadPoolExecutor(max_workers=2) as pool:
                codes = list(pool.map(lambda _: evaluate_once(), range(2)))
        self.assertEqual(sorted(codes), [200, 409])
        self.assertEqual(self.client.get("/api/history").json["interviews"][0]["questions_answered"], 1)

    def test_invalid_payloads_return_useful_client_errors(self):
        self.assertEqual(self.client.post("/api/start", json=["Java"]).status_code, 400)
        self.assertEqual(self.client.post("/api/start", json={"topic": 123}).status_code, 400)
        self.assertEqual(self.client.post("/api/start", json={"topic": "Javascript"}).status_code, 400)

    def test_configured_database_failure_does_not_switch_accounts_to_sqlite(self):
        with patch.object(database, "DATABASE_URL", "postgresql://invalid/test"), \
                patch("psycopg2.connect", side_effect=RuntimeError("unavailable")), \
                patch("sqlite3.connect") as sqlite_connect:
            with self.assertRaisesRegex(RuntimeError, "configured PostgreSQL"):
                database.connect()
            sqlite_connect.assert_not_called()


class GroundingRegressionTests(unittest.TestCase):
    def test_embedding_failure_falls_back_and_normalizes_network_subject(self):
        import grounding
        broken = Mock()
        broken.search.side_effect = RuntimeError("Embedding service unavailable")
        with patch.object(grounding, "_retriever", broken), patch.object(grounding, "_tried_to_build", True):
            text, sources = grounding.get_reference("TCP congestion control", "Computer Networks")
        self.assertTrue(text)
        self.assertTrue(sources)
        self.assertTrue(all(source["chunk_id"].upper().startswith("CN") for source in sources))


if __name__ == "__main__":
    unittest.main()
