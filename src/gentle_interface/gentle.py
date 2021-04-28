"""
gentle.py

Created on 2021-04-28
Updated on 2021-04-28

Copyright © Ryan Kan

Description: The class that will directly interface with the gentle program.
"""

# IMPORTS
import os
import subprocess
import time

import requests


# CLASS
class Gentle:
    """
    The gentle interface.

    This class will directly interface with the gentle server to generate the timetable.
    """

    # Dunder Methods
    def __init__(self):
        """
        Initialisation function.
        """

        # Start the gentle container
        self._start_gentle_container()

    # Methods
    def get_timetable(self, audio_file_path, transcript_path):
        """
        Gets the timetable from the gentle server.

        Args:
            audio_file_path (str):
                Path to the audio file.

            transcript_path (str):
                Path to the transcript.

        Returns:
            dict:
                The timetable.

        Raises:
            FileNotFoundError:
                If either the audio file or the transcript cannot be found.
        """

        # Check if the files exist
        if not os.path.isfile(audio_file_path):
            raise FileNotFoundError(f"The audio file cannot be found at the path '{audio_file_path}'.")
        if not os.path.isfile(transcript_path):
            raise FileNotFoundError(f"The transcript cannot be found at the path '{transcript_path}'.")

        # Generate the `files` dictionary
        files = {
            "audio": (audio_file_path, open(audio_file_path, "rb")),
            "transcript": (transcript_path, open(transcript_path, "rb")),
        }

        # Pass these files to the server as a POST request
        # Todo: perhaps during the processing we show a progress bar by reading the log output of the server?
        response = requests.post(url="http://localhost:8765/transcriptions?async=false", files=files)

        # Check the response code
        response.raise_for_status()
        print(response.text)

        # Todo: process the timetable

    def stop_gentle_container(self):
        """
        Method to stop the gentle container/

        Raises:
            ModuleNotFoundError:
                If the gentle container was not installed.

        """

        output = self._run_cmd("docker stop gentle-container", return_output=False)
        print(output)

    # Helper Methods
    @staticmethod
    def _run_cmd(cmd, mute_output=True, return_output=True):
        """
        Runs a command in the command line.

        Args:
            cmd (str):
                The command to be run.

            mute_output (bool):
                Should the output to stdout and stderr not be shown? Applies only if `return_output` is False.
                (Default = True)

            return_output (bool):
                Whether or not the output from the command should be returned.
                (Default = True)

        Returns:
            union[int, bytes]:
                If `return_output` is False, then the INTEGER returned is the exit code.
                If `return_output` is True, then the BYTES returned is the output of the command.
        """

        if not return_output:
            devnull = open(os.devnull, "w") if mute_output else None
            return subprocess.call(cmd, shell=True, stdout=devnull, stderr=devnull)
        else:
            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            except subprocess.CalledProcessError as e:  # This is no matter; we'll tell the user that it had a EO
                output = e.output

            return output.strip()

    def _start_gentle_container(self):
        """
        Helper method that helps to set up the gentle container.

        Raises:
            ModuleNotFoundError:
                If the gentle docker container was not installed.
        """

        # Attempt to start the gentle container
        output = self._run_cmd("docker start gentle-container", return_output=False)
        time.sleep(1)  # Wait for 1 second for everything to set up correctly

        # Check the exit code of the program
        if output != 0:  # Non-zero exit code
            # Likely because the module is not found
            raise ModuleNotFoundError(f"Starting of gentle container returned non-zero error code {output}: "
                                      f"did you install the gentle docker container?")


# TESTING CODE
if __name__ == "__main__":
    # Create a `Gentle` object
    gentle = Gentle()

    # Try passing it an audio file and a transcript
    gentle.get_timetable("../../TestTranscript.wav", "../../TranscriptClean.txt")

    # Stop the gentle container
    gentle.stop_gentle_container()
