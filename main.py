from question_generator import (
    generate_first_question,
    generate_continuation_question
)
from voice_input import record_audio
from transcriber import transcribe_audio
from evaluator import evaluate_answer
from probe_selector import select_probe_strategy
from followup_generator import generate_followup


def main():

    print("\n========== CRACKPROOF ==========\n")

    # 1. User chooses topic
    topic = input("Enter the topic you want to practice: ")

    # 2. Generate first question
    question = generate_first_question(topic)

    # Stores all interview turns
    interview_history = []

    # For now, maximum 5 questions
    for question_number in range(1, 6):

        print(f"\n========== QUESTION {question_number} ==========")
        print("\nInterviewer:")
        print(question)

        # 3. Candidate answers using microphone
        audio_file = record_audio()

        if audio_file is None:
            print("No audio was recorded.")
            break

        # 4. Voice -> text
        transcript = transcribe_audio(audio_file)

        print("\nCandidate Transcript:")
        print(transcript)

        # 5. Evaluate answer
        evaluation = evaluate_answer(
            question=question,
            transcript=transcript
        )

        # 6. Show evaluation
        print("\n========== EVALUATION ==========")

        print("Verdict:", evaluation.verdict)
        print("Correctness:", evaluation.correctness_score, "/10")
        print("Depth:", evaluation.depth_score, "/10")

        print("\nCorrect Points:")
        for point in evaluation.correct_points:
            print("-", point)

        print("\nMissing Core Concepts:")
        for concept in evaluation.missing_core_concepts:
            print("-", concept)

        print("\nDeeper Concepts To Probe:")
        for concept in evaluation.deeper_concepts_to_probe:
            print("-", concept)

        print("\nMisconceptions:")
        for misconception in evaluation.misconceptions:
            print("-", misconception)

        print("\nReasoning:")
        print(evaluation.reasoning)

        # 7. Decide what should be tested next
        probe = select_probe_strategy(evaluation)

        print("\n========== NEXT PROBE ==========")
        print("Strategy:", probe["strategy"])
        print("Target:", probe["target"])

        # 8. Save this turn in interview history
        interview_history.append({
            "question_number": question_number,
            "question": question,
            "transcript": transcript,
            "evaluation": evaluation,
            "probe_strategy": probe["strategy"],
            "probe_target": probe["target"]
        })

        # Don't generate Q6 after final question
        if question_number == 5:
            break

        # 9. Generate next targeted question
        question = generate_followup(
            topic=topic,
            question=question,
            transcript=transcript,
            probe=probe
          )

        # ==========================================
        # AFTER EVERY 5 QUESTIONS
        # ==========================================

        print("\n========== WHAT WOULD YOU LIKE TO DO? ==========")

        print("1. Continue with the same topic")
        print("2. Choose another topic")
        print("3. End interview")

        choice = input("\nEnter your choice (1/2/3): ")

        # SAME TOPIC
        if choice == "1":

            print(f"\nContinuing with topic: {topic}")

            question = generate_continuation_question(
            topic=topic,
            interview_history=interview_history
    )

        # NEW TOPIC
        elif choice == "2":

            topic = input("\nEnter the new topic you want to practice: ")

            question = generate_first_question(topic)

        # END
        elif choice == "3":

            print("\n========== INTERVIEW COMPLETE ==========")
            print("Total questions answered:", len(interview_history))
            break

        else:
            print("\nInvalid choice. Ending interview.")
            break


if __name__ == "__main__":
    main()