"""Panel workflow regression tests: isolated database, deterministic model replies."""
import io
import os
import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch

import database
import panel_session
import panel_routes
import test_web

PROFILE = {"target_role": "Backend Developer", "experience_level": "Fresher", "skills": ["Python", "SQL"], "projects": []}


class PanelTests(unittest.TestCase):
    setUpClass = classmethod(test_web.WebRegressionTests.setUpClass.__func__)
    setUp = test_web.WebRegressionTests.setUp
    login = test_web.WebRegressionTests.login

    def start_panel(self, client=None, token="test-request-123456"):
        client = client or self.client
        client.post("/api/profile", json=PROFILE)
        response = client.post("/api/panels/start", json={"request_id": token})
        self.assertEqual(response.status_code, 200)
        return response.json["session"]

    def advance(self, panel_id, client=None):
        with patch.object(panel_session, "ask_llm", return_value=panel_session.Question(question="Explain your approach.")):
            response = (client or self.client).post(f"/api/panels/{panel_id}/advance", json={})
        self.assertEqual(response.status_code, 200)
        return response.json["session"]

    def answer(self, panel_id, number=1, answer="I would use a database index.", client=None):
        return (client or self.client).post(f"/api/panels/{panel_id}/answer", json={"question_number": number, "answer": answer})

    def test_start_requires_profile_and_is_idempotent(self):
        self.assertEqual(self.client.post("/api/panels/start", json={"request_id": "test-request-123456"}).status_code, 400)
        state = self.start_panel()
        again = self.start_panel()
        self.assertEqual(state["id"], again["id"])
        self.assertEqual(len(self.client.get("/api/panels").json["sessions"]), 1)
        self.client.post("/api/profile", json={**PROFILE, "skills": ["Java"]})
        saved = self.client.get(f'/api/panels/{state["id"]}').json["session"]
        self.assertEqual(saved["profile"]["skills"], ["Python", "SQL"])

    def test_guest_and_account_isolation(self):
        state = self.start_panel()
        for endpoint in ["", "/answer", "/advance", "/finish", "/transcribe"]:
            method = self.other.get if not endpoint else self.other.post
            self.assertEqual(method(f'/api/panels/{state["id"]}{endpoint}').status_code, 404)
        self.assertEqual(self.other.get("/api/panels").json["sessions"], [])
        self.login(self.client, "panel-owner@example.com")
        self.assertEqual(self.client.get(f'/api/panels/{state["id"]}').status_code, 404)
        account_state = self.start_panel()
        user_id = self.client.get("/api/me").json["user"]["id"]
        database.delete_account(user_id)
        self.assertIsNone(database.load_panel(account_state["id"], "user:" + str(user_id)))

    def test_answer_survives_question_failure_and_retry(self):
        state = self.start_panel()
        panel_id = state["id"]
        self.advance(panel_id)
        self.assertTrue(self.answer(panel_id).json["ok"])
        with patch.object(panel_session, "ask_llm", return_value=None):
            self.assertEqual(self.client.post(f"/api/panels/{panel_id}/advance", json={}).status_code, 502)
        saved = self.client.get(f"/api/panels/{panel_id}").json["session"]
        self.assertEqual(len(saved["turns"]), 1)
        self.assertIsNone(saved["current"])
        self.assertEqual(self.advance(panel_id)["current"]["number"], 2)
        self.assertEqual(len(self.answer(panel_id).json["session"]["turns"]), 1)
        self.assertEqual(self.answer(panel_id, answer="A different stale answer").status_code, 409)

    def test_guest_can_reopen_after_refresh_and_guest_entry(self):
        panel_id = self.start_panel()["id"]
        self.advance(panel_id)
        self.answer(panel_id)
        refreshed = self.server.app.test_client()
        refreshed.set_cookie("session", self.client.get_cookie("session").value)
        refreshed.post("/api/logout", json={})
        saved = refreshed.get(f"/api/panels/{panel_id}")
        self.assertEqual(saved.status_code, 200)
        self.assertEqual(len(saved.json["session"]["turns"]), 1)

    def test_six_turn_rotation_report_retry_and_no_overrun(self):
        panel_id = self.start_panel()["id"]
        for number, persona in enumerate(["technical", "technical", "project", "project", "hiring", "hiring"], 1):
            state = self.advance(panel_id)
            self.assertEqual(state["current"]["persona"], persona)
            self.assertEqual(state["current"]["number"], number)
            state = self.answer(panel_id, number).json["session"]
        self.assertEqual(state["status"], "report_pending")
        self.assertEqual(self.answer(panel_id, 7).status_code, 409)
        invalid_report = panel_session.PanelReport(summary="Practice summary", feedback=[panel_session.TurnFeedback(question_number=1, strength="Clear", improvement="Examples", practice_task="Explain trade-offs")])
        with patch.object(panel_session, "ask_llm", return_value=invalid_report):
            self.assertEqual(self.client.post(f"/api/panels/{panel_id}/advance", json={}).status_code, 502)
        report = panel_session.PanelReport(summary="Practice summary", feedback=[panel_session.TurnFeedback(question_number=n, strength="Clear", improvement="Examples", practice_task="Explain trade-offs") for n in range(1, 7)])
        with patch.object(panel_session, "ask_llm", return_value=report) as ai:
            response = self.client.post(f"/api/panels/{panel_id}/advance", json={})
            self.assertEqual(response.json["session"]["status"], "completed")
            self.client.post(f"/api/panels/{panel_id}/advance", json={})
            ai.assert_called_once()

    def test_early_finish_requires_answer_and_freezes_session(self):
        panel_id = self.start_panel()["id"]
        self.assertEqual(self.client.post(f"/api/panels/{panel_id}/finish", json={}).status_code, 400)
        self.advance(panel_id)
        self.answer(panel_id)
        self.advance(panel_id)
        response = self.client.post(f"/api/panels/{panel_id}/finish", json={})
        self.assertEqual(response.json["session"]["status"], "report_pending")
        self.assertIsNone(response.json["session"]["current"])
        self.assertEqual(self.answer(panel_id, 2).status_code, 409)

    def test_invalid_answers_do_not_mutate_state(self):
        panel_id = self.start_panel()["id"]
        self.advance(panel_id)
        for number, answer in [(True, "answer"), (1, " "), (1, []), (1, "x" * 6001), ("1", "answer")]:
            self.assertEqual(self.answer(panel_id, number, answer).status_code, 400)
        self.assertEqual(self.client.get(f"/api/panels/{panel_id}").json["session"]["turns"], [])

    def test_concurrent_answers_cannot_overwrite(self):
        panel_id = self.start_panel()["id"]
        self.advance(panel_id)
        cookie = self.client.get_cookie("session").value
        barrier = Barrier(2)
        original = database.save_panel
        def synchronized_save(*args, **kwargs):
            barrier.wait(timeout=5)
            return original(*args, **kwargs)
        def answer_from_tab(text):
            client = self.server.app.test_client()
            client.set_cookie("session", cookie)
            return self.answer(panel_id, answer=text, client=client).status_code
        with patch.object(database, "save_panel", side_effect=synchronized_save), ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(answer_from_tab, ["Answer one", "Answer two"]))
        self.assertEqual(sorted(results), [200, 409])
        self.assertEqual(len(self.client.get(f"/api/panels/{panel_id}").json["session"]["turns"]), 1)

    def test_audio_ownership_quality_and_cleanup(self):
        panel_id = self.start_panel()["id"]
        self.advance(panel_id)
        paths = []
        def transcribe(path):
            paths.append(path)
            return "Unclear words", "Audio quality too low"
        with patch.object(panel_routes, "transcribe_audio", side_effect=transcribe):
            response = self.client.post(f"/api/panels/{panel_id}/transcribe", data={"question_number": "1", "audio": (io.BytesIO(b"fake audio"), "answer.wav")})
        self.assertFalse(response.json["ok"])
        self.assertFalse(os.path.exists(paths[0]))
        self.answer(panel_id)
        with patch.object(panel_routes, "transcribe_audio") as ai:
            response = self.client.post(f"/api/panels/{panel_id}/transcribe", data={"question_number": "1", "audio": (io.BytesIO(b"fake audio"), "answer.wav")})
            self.assertEqual(response.status_code, 409)
            ai.assert_not_called()


if __name__ == "__main__":
    unittest.main()
