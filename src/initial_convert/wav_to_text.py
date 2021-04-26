"""
wav_to_text.py

Created on 2021-04-26
Updated on 2021-04-26

Copyright © Ryan Kan

Description: Implements the initial conversion from a WAV file to a string.
"""

# IMPORTS
import os

import speech_recognition as sr


# FUNCTIONS
def wav_to_transcript(wav_file):
    """
    Converts the audio in the WAV file into a string.

    Args:
        wav_file (str):
            Path to the WAV file.

    Returns:
        str:
            The text that the program thinks that the audio contains.

    Raises:
        FileNotFoundError:
            If the file cannot be located or cannot be found.
    """

    # Assert that the file exists
    if not os.path.isfile(wav_file):
        raise FileNotFoundError(f"A WAV file does not exist at the path '{wav_file}'.")

    # Define a recogniser
    recogniser = sr.Recognizer()

    # Open the audio file
    with sr.AudioFile(wav_file) as source:
        # Read the entire file
        audio = recogniser.record(source)

        # Get the transcript
        return recogniser.recognize_google(audio)  # Todo: replace with another transcription service


# DEBUG CODE
if __name__ == "__main__" and os.path.isfile("../../TestTranscript.wav"):
    # Test the transcription service
    transcript = wav_to_transcript("../../TestTranscript.wav")

    with open("transcript.txt", "w+") as f:
        f.write(transcript)

