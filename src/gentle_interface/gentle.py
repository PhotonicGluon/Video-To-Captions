"""
gentle.py

Created on 2021-04-28
Updated on 2021-05-01

Copyright © Ryan Kan

Description: The class that will directly interface with the gentle program.
"""

# IMPORTS
import asyncio
import os
import re
import subprocess
import time

from aiohttp import ClientSession
from tqdm import tqdm


# CLASS
class Gentle:
    """
    The gentle interface.

    This class will directly interface with the gentle server to generate the timetable.
    """

    # Methods
    def start_gentle_container(self):
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

    def stop_gentle_container(self):
        """
        Method to stop the gentle container/

        Raises:
            ModuleNotFoundError:
                If the gentle container was not installed.

        """

        output = self._run_cmd("docker stop gentle-container", return_output=False)
        print(output)

    def get_timetable(self, audio_file_path, transcript_path, refresh_interval=0.1):
        """
        Helper method that gets the timetable from the gentle server.
        This is an asynchronous method.

        Args:
            audio_file_path (str):
                Path to the audio file.

            transcript_path (str):
                Path to the transcript.

            refresh_interval (float):
                Duration in seconds to wait before refreshing the progress bar.
                (Default = 0.1)

        Returns:
            dict:
                The timetable.

        Raises:
            FileNotFoundError:
                If either the audio file or the transcript cannot be found.
        """

        return asyncio.run(self._get_timetable(audio_file_path, transcript_path, refresh_interval=refresh_interval))

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

    def _get_latest_output(self):
        """
        Helper method to get the latest console output from the gentle container.

        Returns:
            str:
                The last line of the console output.
        """

        return self._run_cmd("docker logs gentle-container --tail 1")

    async def _update_progress_bar(self, refresh_interval=0.5):
        """
        Helper method to update the progress bar on the progress of the timetable creation.

        Args:
            refresh_interval (float):
                Duration in seconds to wait before checking for any updates.
                (Default = 0.5)
        """

        # Define a new progress bar object
        progress_bar = tqdm(desc="Transcribing the Audio File")

        # Now continuously get command line output until something like "X/Y" is output
        while True:
            # Get the latest output from the command line
            latest_output = self._get_latest_output()

            # Check if it matches the format
            match = re.search(r"(\d+)/(\d+)", latest_output)

            if match:
                # Break out of the loop
                break

            # If not; wait for another `refresh_interval` seconds before querying again
            await asyncio.sleep(refresh_interval)

        # Get the total number of iterations that needs to be run
        total = int(match.group(2))

        # Update the total on the progress bar
        progress_bar.reset(total=total)
        progress_bar.update(1)  # One iteration has already been run

        # Continue reading from console output until `total` outputs have been received in total
        num_outputs = 1
        while num_outputs < total - 1:  # We'll need to handle the last iteration separately
            # Wait for another `refresh_interval` seconds before querying again
            await asyncio.sleep(refresh_interval)

            # Get the latest output from the command line
            latest_output = self._get_latest_output()

            # Get the matching group and update from there
            match = re.search(r"(\d+)/(\d+)", latest_output)
            new_progress = int(match.group(1))  # This is the current progress
            num_to_update_by = new_progress - num_outputs

            progress_bar.update(num_to_update_by)
            num_outputs = new_progress

        # The last iteration would be handled here
        progress_bar.update(2)

    async def _get_timetable(self, audio_file_path, transcript_path, refresh_interval=0.5):
        """
        Helper method that gets the timetable from the gentle server.
        This is an asynchronous method.

        Args:
            audio_file_path (str):
                Path to the audio file.

            transcript_path (str):
                Path to the transcript.

            refresh_interval (float):
                Duration in seconds to wait before refreshing the progress bar.
                (Default = 0.5)

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
            "audio": open(audio_file_path, "rb"),
            "transcript": open(transcript_path, "rb"),
        }

        # Create the progress bar task
        progress_bar_task = asyncio.create_task(self._update_progress_bar(refresh_interval=refresh_interval))

        # Create the file passing task
        async def __request_post_helper():
            async with ClientSession() as session:
                return await session.post(url="http://localhost:8765/transcriptions?async=false", data=files)

        file_passing_task = asyncio.create_task(__request_post_helper())

        # Wait for completion of both tasks
        response = await file_passing_task
        await progress_bar_task

        # Check the response code
        response.raise_for_status()
        print(response.text)

        # Todo: process the timetable


# TESTING CODE
if __name__ == "__main__":
    # Create a `Gentle` object
    gentle = Gentle()

    # Start the gentle container
    gentle.start_gentle_container()

    # Try passing it an audio file and a transcript
    gentle.get_timetable("../../TestTranscript.wav", "../../TranscriptClean.txt")

    # Stop the gentle container
    gentle.stop_gentle_container()
