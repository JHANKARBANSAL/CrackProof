import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

def record_audio(filename="recordings/answer1.wav"):

    # Create whatever folder the caller asked for, not a hardcoded one
    directory = os.path.dirname(filename)

    if directory:
        os.makedirs(directory, exist_ok=True)

    sample_rate = 44100
    recorded_chunks = []

    # This function receives microphone audio continuously
    def callback(indata, frames, time, status):

        if status:
            print("Audio status:", status)

        # IMPORTANT:
        # Save every incoming chunk
        recorded_chunks.append(indata.copy())


    input("\nPress ENTER to START recording...")

    print("\n🎤 RECORDING STARTED")
    print("Speak your answer.")
    print("Press ENTER when you want to STOP.\n")


    with sd.InputStream(
        device=0,              # Your MacBook Air Microphone
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        callback=callback
    ):

        # Program keeps recording until you press Enter
        input()


    print("⏹️ Recording stopped.")


    if len(recorded_chunks) == 0:
        print("❌ No audio captured.")
        return None


    # Combine all recorded chunks
    audio = np.concatenate(recorded_chunks, axis=0)


    # Check whether microphone actually captured sound
    max_amplitude = np.max(np.abs(audio))

    print("Maximum amplitude:", max_amplitude)


    # Convert float audio to 16-bit WAV
    audio_int16 = np.int16(
        np.clip(audio, -1, 1) * 32767
    )


    write(
        filename,
        sample_rate,
        audio_int16
    )


    print(f"✅ Recording saved to: {filename}")

    return filename


