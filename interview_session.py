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

from question_generator import (
    generate_first_question,
    generate_continuation_question
)
from transcriber import transcribe_audio
from evaluator import evaluate_answer
from probe_selector import select_probe_strategy
from followup_generator import generate_followup
from grounding import get_reference
from reporting import build_report


RECORDINGS_DIR = "recordings"

QUESTIONS_PER_BATCH = 5


class InterviewSession:

    def __init__(self, topic):

        self.topic = topic

        self.interview_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.folder = os.path.join(
            RECORDINGS_DIR,
            "interview_" + self.interview_id
        )

        os.makedirs(self.folder, exist_ok=True)

        self.history = []

        # Ye kabhi reset nahi hota, topic badalne par bhi
        self.question_number = 0

        # Is batch ke turns history mein kahan se shuru hote hain
        self.batch_start = 0

        # Ek hi sawaal ke kitne attempts ho chuke (retry ke liye)
        self.attempt = 0

        self.question = generate_first_question(topic)

        self.finished = False

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
            "question_number": self.question_number + 1,
            "batch_position": len(self.history) - self.batch_start + 1,
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
                    "Your recording is saved."
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
        }

        self.history.append(turn)
        self.save()

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

        if not self.history:
            return self.current_question()

        last = self.history[-1]

        self.question = generate_followup(
            topic=self.topic,
            question=last["question"],
            transcript=last["transcript"],
            probe={
                "strategy": last["probe_strategy"],
                "target": last["probe_target"],
            }
        )

        return self.current_question()

    def continue_same_topic(self):
        """Batch khatam hone ke baad usi topic par aage badho."""

        self.batch_start = len(self.history)

        self.question = generate_continuation_question(
            topic=self.topic,
            interview_history=self.history
        )

        return self.current_question()

    def change_topic(self, topic):
        """
        Naya topic. Question numbering phir bhi reset nahi hoti -
        ye ek hi interview session hai.
        """

        self.topic = topic
        self.batch_start = len(self.history)

        self.question = generate_first_question(topic)

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

        batch = self.history[self.batch_start:]

        self.finished = True

        return as_plain_report(build_report(batch))

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
