"""
get_timetable.py

Created on 2021-05-02
Updated on 2021-05-03

Copyright © Ryan Kan

Description: Gets the timetable of spoken words from the audio file.
"""

# IMPORTS
import os

from src.gentle_interface.gentle import Gentle


# FUNCTIONS
def get_timetable(audio_file_path, transcript_path, refresh_interval=0.5):
    """
    Gets the timetable of spoken words from the audio file and transcript file.

    Args:
        audio_file_path (str):
            Path to the audio file.

        transcript_path (str):
            Path to the transcript.

        refresh_interval (float):
            Duration in seconds to wait before refreshing the progress bar.
            (Default = 0.1)

    Returns:
        list[dict]:
            The timetable of spoken words.

    Raises:
        FileNotFoundError:
            If either the audio file or the transcript cannot be found.
    """

    # Check if the files exist
    if not os.path.isfile(audio_file_path):
        raise FileNotFoundError(f"The audio file cannot be found at the path '{audio_file_path}'.")
    if not os.path.isfile(transcript_path):
        raise FileNotFoundError(f"The transcript cannot be found at the path '{transcript_path}'.")

    # Create a `Gentle` object
    gentle = Gentle()

    # Start the gentle container
    gentle.start_gentle_container()

    # Get the timetable
    timetable = gentle.get_timetable(audio_file_path, transcript_path, refresh_interval=refresh_interval)

    # Stop the gentle container
    gentle.stop_gentle_container()

    # Return the timetable
    return timetable


# TESTING CODE
if __name__ == "__main__":
    # Try passing it an audio file and a transcript
    myTimetable = get_timetable("../../TestTranscript.wav", "../../TranscriptClean.txt")
    print(myTimetable)
