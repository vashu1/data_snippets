#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
from pathlib import Path
import random

from openai import OpenAI


def generate_sentence(client: OpenAI, word: str) -> str:
    response = client.responses.create(
        model="gpt-5.2",
        instructions=(
            "Generate exactly one short, natural English sentence using the given word. "
            "The sentence should be useful for pronunciation practice. "
            "Return only the sentence, no explanation."
        ),
        input=f"Word: {word}",
    )

    sentence = response.output_text.strip()

    # Basic cleanup in case the model returns quotes.
    sentence = sentence.strip('"').strip("'").strip()

    return sentence


def make_speech_file(client: OpenAI, text: str, output_path: Path) -> None:
    # OpenAI Speech API generates audio from input text.
    # gpt-4o-mini-tts supports voice control via instructions.
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instructions="Speak clearly and naturally, as in an English pronunciation lesson.",
        response_format="mp3",
    )

    output_path.write_bytes(response.read())


def play_audio(path: Path) -> None:
    system = platform.system()

    if system == "Darwin":  # macOS
        subprocess.run(["afplay", str(path)], check=False)
    elif system == "Windows":
        os.startfile(path)  # type: ignore[attr-defined]
    elif system == "Linux":
        # Requires xdg-utils; works on many desktop Linux installs.
        subprocess.run(["xdg-open", str(path)], check=False)
    else:
        print(f"Audio saved to: {path}")
        print("Automatic playback is not supported on this OS.")


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Please set OPENAI_API_KEY first.")

    #word = " ".join(sys.argv[1:]).strip()
    #if not word:
    #    word = input("Enter a word: ").strip()
    #if not word:
    #    raise ValueError("No word provided.")

    words = open('word_list.txt').readlines()
    words = [i.strip() for i in words]
    random.shuffle(words)

    client = OpenAI()

    for word in words:
	    sentence = generate_sentence(client, word)
	    #print(f"Sentence: {sentence}")
	    safe_word = "".join(c for c in word.lower() if c.isalnum() or c in ("-", "_")) or "word"
	    output_path = Path(f"audio/pronunciation_{safe_word}.mp3")
	    make_speech_file(client, word + '   ' + sentence, output_path)
	    #print(f"Saved audio: {output_path.resolve()}")
	    play_audio(output_path)
	    _ = input()


if __name__ == "__main__":
    main()