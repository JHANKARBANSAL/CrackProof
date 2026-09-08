import whisper

print("Loading Whisper model...")

model = whisper.load_model("small")


def transcribe_audio(audio_path):
    print("Converting speech to text locally...")

    result = model.transcribe(audio_path)

    return result["text"]


# TEST
text = transcribe_audio("recordings/answer1.wav")

print("\nCandidate said:")
print(text)