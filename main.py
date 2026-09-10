import json
import os
from datetime import datetime

from question_generator import (
    generate_first_question,
    generate_continuation_question
)
from voice_input import record_audio
from transcriber import transcribe_audio
from evaluator import evaluate_answer
from probe_selector import select_probe_strategy
from followup_generator import generate_followup
from llm_client import describe as describe_llm
from grounding import get_reference
from reporting import build_report
from display import (
    show_reference,
    show_evaluation,
    show_probe,
    show_report,
)


def save_history(interview_folder, interview_history):
    """
    Write the interview so far to a JSON file next to its recordings.

    Called after every completed answer, so a crash, a Ctrl+C, or a
    closed terminal can never destroy work the candidate already did.
    Saving must never break the interview, so any error here is
    reported and ignored.
    """

    path = os.path.join(interview_folder, "interview_history.json")

    try:
        rows = []

        for turn in interview_history:

            row = dict(turn)

            # The evaluation is a Pydantic object, so turn it into
            # plain data that JSON can store.
            row["evaluation"] = turn["evaluation"].model_dump()

            rows.append(row)

        with open(path, "w") as history_file:
            json.dump(rows, history_file, indent=2)

    except Exception as error:
        print("  Could not save interview history:", error)


def generate_and_print_report(current_batch):
    """
    Ek batch ka report banao aur dikhao.

    Kaam do hisson mein banta hai:
      reporting.build_report -> data
      display.show_report    -> terminal pe dikhao

    UI aage isi build_report ka data leke apne tareeke se dikhayegi.
    """

    report = build_report(current_batch)

    show_report(report)


def main():

    print("\n========== CRACKPROOF ==========\n")

    # ---------------------------------------
    # ONE UNIQUE SESSION PER INTERVIEW RUN
    # ---------------------------------------

    interview_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    interview_folder = os.path.join(
        "recordings",
        f"interview_{interview_id}"
    )

    os.makedirs(interview_folder, exist_ok=True)

    print("Interview ID:", interview_id)
    print("Model:", describe_llm())

    # User chooses starting topic
    topic = input("\nEnter the topic you want to practice: ").strip()

    # Stores complete interview history
    interview_history = []

    # Never resets, even when the topic changes
    global_question_number = 0

    # Generate first question
    question = generate_first_question(topic)

    if question is None:
        print(
            "\nCould not generate the first question. "
            "Please check your internet connection and try again."
        )
        return

    while True:

        # Where this batch begins inside interview_history, so an
        # early stop reports on THIS batch only and never bleeds
        # into the previous one.
        batch_start_index = len(interview_history)

        stop_requested = False

        # Ask 5 questions for the current topic
        for batch_question_number in range(1, 6):

            global_question_number += 1

            print(
                f"\n========== QUESTION "
                f"{global_question_number} =========="
            )

            print("\nInterviewer:")
            print(question)

            # ---------------------------------------
            # 1. RECORD CANDIDATE ANSWER
            # ---------------------------------------

            # Retry the SAME question until we get a usable
            # transcript. A failed attempt is not a completed
            # question, so global_question_number does not move.

            attempt = 0

            while True:

                attempt += 1

                if attempt == 1:
                    wav_name = (
                        f"question_"
                        f"{global_question_number:02d}.wav"
                    )
                else:
                    # Keep the failed audio instead of overwriting it
                    wav_name = (
                        f"question_"
                        f"{global_question_number:02d}"
                        f"_retry{attempt - 1}.wav"
                    )

                audio_filename = os.path.join(
                    interview_folder,
                    wav_name
                )

                audio_file = record_audio(filename=audio_filename)

                if audio_file is None:
                    print(
                        "\nNo audio was recorded. "
                        "Ending the interview here."
                    )
                    # Report on whatever was completed instead of
                    # throwing the finished answers away.
                    stop_requested = True
                    break

                # ---------------------------------------
                # 2. SPEECH -> TEXT
                # ---------------------------------------

                transcript, problem = transcribe_audio(audio_file)

                if problem is None:
                    break

                # Transcript bharose ke laayak nahi hai. Wajah batao
                # aur wahi sawaal dobara record karwao. Ye ek poora
                # sawaal nahi ginta, isliye numbering nahi hilti.
                print("\n" + problem)
                print(
                    "Please record the answer again."
                )

            # The microphone failed, so leave the question loop too.
            if stop_requested:
                break

            print("\nCandidate Transcript:")
            print(transcript)

            # ---------------------------------------
            # 3. EVALUATE ANSWER
            # ---------------------------------------

            # Knowledge base se is sawaal ka reference text laao.
            # Na mile to khaali aayega aur evaluation waise hi
            # chalegi jaise pehle chalti thi.
            reference, sources = get_reference(question, topic)

            show_reference(sources)

            evaluation = evaluate_answer(
                question=question,
                transcript=transcript,
                reference=reference
            )

            if evaluation is None:
                print(
                    "\nThis answer could not be evaluated. "
                    "Your recording is saved, and the report below "
                    "covers the answers completed so far."
                )
                stop_requested = True
                break

            show_evaluation(evaluation, sources)

            # ---------------------------------------
            # 5. SELECT NEXT PROBE
            # ---------------------------------------

            probe = select_probe_strategy(evaluation)

            show_probe(probe)

            # ---------------------------------------
            # 6. SAVE COMPLETE INTERVIEW TURN
            # ---------------------------------------

            interview_history.append({
                "interview_id": interview_id,
                "topic": topic,
                "question_number": global_question_number,
                "question": question,
                "transcript": transcript,
                "evaluation": evaluation,
                "probe_strategy": probe["strategy"],
                "probe_target": probe["target"],
                "audio_file": audio_file,

                # Ye evaluation reference ke saath hui thi ya nahi.
                # Baad mein naap sakte hain ki grounding se farak
                # pada ya nahi.
                "grounded": bool(sources),
                "reference_sources": sources
            })

            # Save immediately so this answer cannot be lost
            save_history(interview_folder, interview_history)

            # Question 5 of this batch complete -> stop this batch
            if batch_question_number == 5:
                break

            # ---------------------------------------
            # 7. INTERVIEW CONTROL
            #
            # Asked only AFTER an answer is completed and recording
            # has finished. Stopping is not a question: it does not
            # touch global_question_number and appends no turn.
            # ---------------------------------------

            print("\n[C] Continue Interview")
            print("[S] Stop & Generate Report")

            control = input("Your choice (C/S): ").strip().lower()

            while control not in ("c", "s", ""):
                print("Please enter C or S.")
                control = input("Your choice (C/S): ").strip().lower()

            if control == "s":
                stop_requested = True
                break

            # ---------------------------------------
            # 8. GENERATE ADAPTIVE FOLLOW-UP
            # ---------------------------------------

            question = generate_followup(
                topic=topic,
                question=question,
                transcript=transcript,
                probe=probe
            )

            if question is None:
                print(
                    "\nThe next question could not be generated. "
                    "The report below covers the answers completed "
                    "so far."
                )
                stop_requested = True
                break

        # ===========================================
        # BATCH REPORT (normal completion OR early stop)
        # ===========================================

        # Only this batch's turns, never the previous batch's.
        current_batch = interview_history[batch_start_index:]

        generate_and_print_report(current_batch)

        # Stop & Generate Report ends the session; do not ask another
        # question or offer the continue/change-topic menu.
        if stop_requested:

            print("\n========== INTERVIEW COMPLETE ==========")
            print("Interview ID:", interview_id)
            print(
                "Total questions answered:",
                len(interview_history)
            )
            print("Recordings saved in:", interview_folder)

            break

        print("\n========== WHAT WOULD YOU LIKE TO DO? ==========")
        print("1. Continue with the same topic")
        print("2. Choose another topic")
        print("3. End interview")

        choice = input("\nEnter your choice (1/2/3): ").strip()

        # ---------------------------------------
        # CONTINUE SAME TOPIC
        # ---------------------------------------

        if choice == "1":

            print(f"\nContinuing with topic: {topic}")

            question = generate_continuation_question(
                topic=topic,
                interview_history=interview_history
            )

            if question is None:
                print(
                    "\nCould not generate the next question. "
                    "Ending the interview here; your completed "
                    "answers are saved."
                )
                break

        # ---------------------------------------
        # CHANGE TOPIC
        # ---------------------------------------

        elif choice == "2":

            topic = input(
                "\nEnter the new topic you want to practice: "
            ).strip()

            question = generate_first_question(topic)

            if question is None:
                print(
                    "\nCould not generate a question for that topic. "
                    "Ending the interview here; your completed "
                    "answers are saved."
                )
                break

        # ---------------------------------------
        # END INTERVIEW
        # ---------------------------------------

        elif choice == "3":

            print("\n========== INTERVIEW COMPLETE ==========")
            print("Interview ID:", interview_id)
            print(
                "Total questions answered:",
                len(interview_history)
            )
            print("Recordings saved in:", interview_folder)

            if interview_history:

                last_turn = interview_history[-1]

                print("\n========== LAST INTERACTION ==========")
                print("Question:", last_turn["question"])
                print("Audio:", last_turn["audio_file"])
                print("Transcript:", last_turn["transcript"])

            break

        else:

            print("\nInvalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        # Every completed answer was already written to
        # interview_history.json, so nothing is lost here.
        print("\n\nInterview stopped.")
        print("Your completed answers and recordings are saved.")