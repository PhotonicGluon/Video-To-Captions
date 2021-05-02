"""
video_to_wav.py

Created on 2021-04-26
Updated on 2021-04-26

Copyright © Ryan Kan

Description: Converts a video file into a WAV file.
"""

# IMPORTS
import os

from pydub import AudioSegment

# CONSTANTS
SUPPORTED_VIDEO_EXTENSIONS = {
    ".mp4": "mp4",
    ".wma": "wma",
    ".aiff": "aac"
}


# FUNCTIONS
def video_to_wav(video_file, wav_file_name="transcript"):
    """
    Converts a video file into a WAV file for further processing.

    Args:
        video_file (str):
            Path to the video file.

        wav_file_name (str):
            Name of the exported WAV file, without the extension ".wav".
            (Default = "transcript")

    Returns:
        str:
            Path to the WAV file.

    Raises:
        AssertionError:
            If the extension of the video file is not in the `SUPPORTED_VIDEO_EXTENSIONS` dictionary.

        FileNotFoundError:
            If the video file does not exist or is not found.
    """

    # Check if the video file exists
    if not os.path.isfile(video_file):
        raise FileNotFoundError(f"A video file does not exist at the path '{video_file}'.")

    # Check if the video file's extension works
    extension = os.path.splitext(video_file)[-1]

    if extension not in SUPPORTED_VIDEO_EXTENSIONS:
        raise AssertionError(f"The extension {extension} is currently unsupported by the program.")

    # Convert the video file into a WAV file
    AudioSegment.from_file(video_file, SUPPORTED_VIDEO_EXTENSIONS[extension]).export(f"{wav_file_name}.wav", "wav")

    # Return the path to the WAV file
    return f"{wav_file_name}.wav"


# DEBUG CODE
if __name__ == "__main__" and os.path.isfile("../../TestVideo.mp4"):  # There is a test video
    # Test the exporting code
    video_to_wav("../../TestVideo.mp4", wav_file_name="TestTranscript")
