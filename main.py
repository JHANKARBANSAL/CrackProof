from question_generator import generate_first_question
from voice_input import record_audio
from transcriber import transcribe_audio
from evaluator import evaluate_answer
from probe_selector import select_probe_strategy
from followup_generator import generate_followup

def main():

    print("\n========== CRACKPROOF ==========\n")

    # 1. User chooses the topic
    topic = input("Enter the topic you want to practice: ")

    # 2. Gemini generates the first question
    question = generate_first_question(topic)

    print("\nInterviewer:")
    print(question)

    # 3. Candidate answers using microphone
    audio_file = record_audio()

    if audio_file is None:
        print("No audio was recorded.")
        return

    # 4. Whisper converts voice -> text
    transcript = transcribe_audio(audio_file)

    print("\nCandidate Transcript:")
    print(transcript)

    # 5. Gemini evaluates the answer
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

    probe = select_probe_strategy(evaluation)

    print("\n========== NEXT PROBE ==========")
    print("Strategy:", probe["strategy"])
    print("Target:", probe["target"])

     # 7. Generate targeted follow-up question
    followup_question = generate_followup(
        topic=topic,
        question=question,
        transcript=transcript,
        probe=probe
    )

    print("\n========== FOLLOW-UP QUESTION ==========")
    print(followup_question)


if __name__ == "__main__":
    main()