"""
wav_to_text.py

Created on 2021-04-26
Updated on 2021-04-27

Copyright © Ryan Kan

Description: Implements the initial conversion from a WAV file to a string.

Todo:
    - Either depreciate this or make the captions generator work better.
"""

# IMPORTS
import math
import os

import speech_recognition as sr
from tqdm import trange

# CONSTANTS
SPEECH_PROCESSING_BLOCK_LENGTH = 10  # Every X seconds of audio will form one block, which will be processed.


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
            (Note: the text here is very 'dirty' and manual editing of the transcript file is needed.)

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
        # Record the audio from the audio file
        audio = recogniser.record(source)

        # Get the length of the audio file
        audio_duration = source.DURATION

        # Determine the number of blocks there will be
        num_blocks = int(math.ceil(audio_duration / SPEECH_PROCESSING_BLOCK_LENGTH))

        # Process each block and append it to the global transcript
        transcript = ""

        for block_num in trange(num_blocks, desc="Processing Audio Blocks"):
            # Get that block's audio
            block_audio = audio.get_segment(start_ms=block_num * SPEECH_PROCESSING_BLOCK_LENGTH * 1000,
                                            end_ms=(block_num + 1) * SPEECH_PROCESSING_BLOCK_LENGTH * 1000)

            # Get the transcript for that block
            try:
                block_transcript = recogniser.recognize_google(block_audio, language="en")
            except sr.UnknownValueError:
                raise sr.UnknownValueError("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                raise sr.RequestError(f"Could not request results from Google Speech Recognition service; {e}")

            # Add that block's transcript to the global transcript
            transcript += block_transcript

            if block_num != num_blocks - 1:
                transcript += " "

        # Return the global transcript
        return transcript


# DEBUG CODE
if __name__ == "__main__" and os.path.isfile("../../TestTranscript.wav"):
    # Test the transcription service
    possibleTranscript = wav_to_transcript("../../TestTranscript.wav")

    with open("../../transcript.txt", "w+") as f:
        f.write(possibleTranscript)
