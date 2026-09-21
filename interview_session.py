"""
Ek interview ka state rakhta hai, step-by-step chalne ke liye.

main.py terminal ke liye hai - usme input() aur print() hain, jo
browser se nahi chal sakte. Ye file wahi interview logic deti hai
par TUKDON MEIN, taaki web server ek-ek kadam chala sake:

    session = InterviewSession("DBMS")
    session.current_question()        -> sawaal
    session.transcribe(wav_path)      -> transcript
    session.evaluate(transcript)      -> evaluation
    session.next_question()           -> agla sawaal
    session.report()                  -> batch report

Ye kuch print nahi karti. Sab kuch return karti hai, taaki UI apne
tareeke se dikha sake.

main.py ise abhi use nahi karta - woh apne aap chalta rehta hai.
Dono ek hi neeche wale modules par khade hain.
"""

import json
import os
from datetime import datetime
from uuid import uuid4

from question_generator import (
    generate_first_question,
    generate_continuation_question
)
from transcriber import transcribe_audio
from evaluator import evaluate_answer, AnswerEvaluation
from probe_selector import select_probe_strategy
from followup_generator import generate_followup
from grounding import get_reference
from reporting import build_report
from depth_aggregator import aggregate_depth_evidence
from assessment_metrics import calculate_batch_metrics


RECORDINGS_DIR = "recordings"

QUESTIONS_PER_BATCH = 5


class InterviewSession:

    def __init__(self, topic):

        self.topic = topic

        self.interview_id = uuid4().hex
        self.created_at = datetime.now().isoformat()

        self.folder = os.path.join(
            RECORDINGS_DIR,
            "interview_" + self.interview_id
        )

        self.history = []

        # Ye kabhi reset nahi hota, topic badalne par bhi
        self.question_number = 0

        # Is batch ke turns history mein kahan se shuru hote hain
        self.batch_start = 0

        # Ek hi sawaal ke kitne attempts ho chuke (retry ke liye)
        self.attempt = 0

        self.question = generate_first_question(topic)

        self.finished = False
        self.question_evaluated = False
        self.report_cache = None

    def snapshot(self):
        return {
            "interview_id": self.interview_id, "created_at": self.created_at,
            "topic": self.topic, "question": self.question,
            "question_number": self.question_number, "batch_start": self.batch_start,
            "attempt": self.attempt, "finished": self.finished,
            "question_evaluated": self.question_evaluated, "report_cache": self.report_cache,
            "history": [dict(t, evaluation=t["evaluation"].model_dump()) for t in self.history],
        }

    @classmethod
    def restore(cls, state):
        """Restore saved state without generating a new question."""
        obj = cls.__new__(cls)
        for key, value in state.items():
            setattr(obj, key, value)
        obj.folder = os.path.join(RECORDINGS_DIR, "interview_" + obj.interview_id)
        obj.history = [dict(t, evaluation=AnswerEvaluation.model_validate(t["evaluation"]))
                       for t in state["history"]]
        return obj

    def saved_report(self):
        """A useful partial report, even before the final narrative is generated."""
        if not self.history:
            return None
        profile = aggregate_depth_evidence(self.history)
        return dict(self.report_cache or {
            "ok": True, "topic": self.topic, "depth_profile": profile,
            "metrics": calculate_batch_metrics(self.history, profile),
            "assessment": None, "in_progress": True,
            "limited_evidence": len(self.history) < QUESTIONS_PER_BATCH,
        }, interview_id=self.interview_id, turns=self.snapshot()["history"])

    # ----------------------------------------------------
    # SAWAAL
    # ----------------------------------------------------

    def current_question(self):
        """Abhi kaunsa sawaal chal raha hai."""

        if self.question is None:
            return {
                "ok": False,
                "message": (
                    "Could not generate a question. "
                    "Please check your connection and try again."
                ),
            }

        return {
            "ok": True,
            "interview_id": self.interview_id,
            "topic": self.topic,
            "question": self.question,
            "question_number": self.question_number if self.question_evaluated else self.question_number + 1,
            "batch_position": len(self.history) - self.batch_start + (0 if self.question_evaluated else 1),
            "questions_per_batch": QUESTIONS_PER_BATCH,
        }

    def audio_path(self, extension="wav"):
        """
        Is attempt ki recording kahan save hogi.

        Pehla attempt seedha question_07.wav. Retry alag naam se,
        taaki fail hui recording mite nahi.

        Browser aksar webm bhejta hai, isliye extension badal sakti hai.
        """

        number = self.question_number + 1

        if self.attempt == 0:
            name = "question_%02d.%s" % (number, extension)
        else:
            name = "question_%02d_retry%d.%s" % (
                number, self.attempt, extension
            )

        return os.path.join(self.folder, name)

    # ----------------------------------------------------
    # AWAAZ -> TEXT
    # ----------------------------------------------------

    def transcribe(self, audio_path):
        """
        Recording ko text banata hai aur batata hai ki bharose ke
        laayak hai ya nahi.

        problem set ho to UI ko wahi sawaal dobara record karwana
        chahiye. Uske liye retry() bulao.
        """

        transcript, problem = transcribe_audio(audio_path)

        return {
            "ok": problem is None,
            "transcript": transcript,
            "problem": problem,
            "audio_path": audio_path,
        }

    def retry(self):
        """
        Wahi sawaal dobara record karne ke liye.

        Ye ek poora sawaal nahi ginta, isliye question_number nahi
        badhta aur history mein kuch nahi jaata.
        """

        self.attempt = self.attempt + 1

    # ----------------------------------------------------
    # EVALUATION
    # ----------------------------------------------------

    def evaluate(self, transcript, audio_path):
        """
        Answer ko reference ke saath judge karta hai aur turn ko
        history mein daal deta hai.
        """

        if self.finished:
            return {"ok": False, "message": "This interview has ended. Please start a new interview."}
        if self.question_evaluated:
            return self.evaluation_response()

        reference, sources = get_reference(self.question, self.topic)

        evaluation = evaluate_answer(
            question=self.question,
            transcript=transcript,
            reference=reference
        )

        if evaluation is None:
            return {
                "ok": False,
                "message": (
                    "This answer could not be evaluated. "
                    "Your transcript is still available. Please try again."
                ),
            }

        probe = select_probe_strategy(evaluation)

        # Ab ye ek poora sawaal ban gaya
        self.question_number = self.question_number + 1
        self.attempt = 0

        turn = {
            "interview_id": self.interview_id,
            "topic": self.topic,
            "question_number": self.question_number,
            "question": self.question,
            "transcript": transcript,
            "evaluation": evaluation,
            "probe_strategy": probe["strategy"],
            "probe_target": probe["target"],
            "audio_file": audio_path,
            "grounded": bool(sources),
            "reference_sources": sources,
            "timestamp": datetime.now().isoformat(),
        }

        self.history.append(turn)
        self.question_evaluated = True
        self.report_cache = None
        return self.evaluation_response()

    def evaluation_response(self):
        turn = self.history[-1]
        evaluation, sources = turn["evaluation"], turn["reference_sources"]

        return {
            "ok": True,
            "evaluation": as_plain_data(evaluation, sources),
            "sources": sources,
            "batch_position": len(self.history) - self.batch_start,
            "batch_complete": (
                len(self.history) - self.batch_start >= QUESTIONS_PER_BATCH
            ),
        }

    # ----------------------------------------------------
    # AGLA SAWAAL
    # ----------------------------------------------------

    def next_question(self):
        """Pichhle answer ke gap par agla sawaal banata hai."""

        if self.finished:
            return {"ok": False, "message": "This interview has ended."}
        if not self.history or not self.question_evaluated:
            return self.current_question()
        if len(self.history) - self.batch_start >= QUESTIONS_PER_BATCH:
            return {"ok": False, "message": "This batch is complete. Please view your report."}

        last = self.history[-1]

        question = generate_followup(
            topic=self.topic,
            question=last["question"],
            transcript=last["transcript"],
            probe={
                "strategy": last["probe_strategy"],
                "target": last["probe_target"],
            }
        )

        if not question:
            return {"ok": False, "message": "Could not generate the next question. Please try again."}
        self.question = question
        self.question_evaluated = False
        return self.current_question()

    def continue_same_topic(self):
        """Batch khatam hone ke baad usi topic par aage badho."""

        if not self.finished:
            return {"ok": False, "message": "Finish the current batch before continuing."}
        question = generate_continuation_question(
            topic=self.topic,
            interview_history=self.history
        )

        if not question:
            return {"ok": False, "message": "Could not generate a question. Please try again."}
        self.question = question
        self.batch_start = len(self.history)
        self.finished = False
        self.question_evaluated = False
        self.report_cache = None
        return self.current_question()

    def change_topic(self, topic):
        """
        Naya topic. Question numbering phir bhi reset nahi hoti -
        ye ek hi interview session hai.
        """

        if not self.finished:
            return {"ok": False, "message": "Finish the current batch before changing topics."}
        question = generate_first_question(topic)
        if not question:
            return {"ok": False, "message": "Could not generate a question. Please try again."}
        self.topic = topic
        self.batch_start = len(self.history)

        self.question = question
        self.finished = False
        self.question_evaluated = False
        self.report_cache = None

        return self.current_question()

    # ----------------------------------------------------
    # REPORT
    # ----------------------------------------------------

    def report(self):
        """
        Is batch ka report. Sirf poore ho chuke answers par.

        Chahe candidate ne beech mein rok diya ho, chahe paanchon
        kar liye hon - dono mein yahi chalta hai.
        """

        if self.report_cache:
            return self.report_cache
        result = as_plain_report(build_report(self.history[self.batch_start:]))
        if result.get("ok"):
            result["interview_id"] = self.interview_id
            self.finished = True
            self.report_cache = result
        return result

    # ----------------------------------------------------
    # SAVE
    # ----------------------------------------------------

    def save(self):
        """
        Har answer ke baad disk par likh do, taaki server band ho
        jaye tab bhi kaam na jaye.
        """

        path = os.path.join(self.folder, "interview_history.json")

        try:
            os.makedirs(self.folder, exist_ok=True)
            rows = []

            for turn in self.history:
                row = dict(turn)
                row["evaluation"] = turn["evaluation"].model_dump()
                rows.append(row)

            with open(path, "w") as f:
                json.dump(rows, f, indent=2)

        except Exception as error:
            print("  Could not save interview history:", error)


# --------------------------------------------------------
# PYDANTIC -> PLAIN DATA
#
# Browser ko JSON chahiye, Pydantic object nahi. Ye function
# usko normal dictionary bana deta hai, aur har claim ke saath
# uska source bhi jod deta hai taaki UI ko dobara na dhoondhna pade.
# --------------------------------------------------------

def as_plain_data(evaluation, sources):

    data = evaluation.model_dump()
    data["sources"] = sources

    source_by_number = {}
    for source in sources:
        source_by_number[source["number"]] = source

    # claim -> source
    claim_source = {}

    for citation in evaluation.citations:
        source = source_by_number.get(citation.source_number)
        if source:
            claim_source[citation.claim.strip().lower()] = source

    def with_source(items):
        out = []
        for item in items:
            out.append({
                "text": item,
                "source": claim_source.get(item.strip().lower()),
            })
        return out

    data["missing_core_concepts"] = with_source(
        evaluation.missing_core_concepts
    )
    data["misconceptions"] = with_source(evaluation.misconceptions)

    return data


def as_plain_report(report):
    """Report ke andar ka Pydantic object bhi plain data banao."""

    if not report.get("ok"):
        return report

    out = dict(report)

    if report.get("assessment") is not None:
        out["assessment"] = report["assessment"].model_dump()

    return out
