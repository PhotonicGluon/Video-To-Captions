"""
transcript_aligner.py

Created on 2021-05-02
Updated on 2021-05-02

Copyright © Ryan Kan

Description: Uses the timetable and transcript to align text according to a certain rule.
"""

# IMPORTS
import re
from math import ceil


# CLASS
class Aligner:
    """
    Class that does the aligning of text according to a rule.
    """

    # Dunder methods
    def __init__(self, transcript, timetable):
        """
        Initialisation method.

        Args:
            transcript (str):
                The raw transcript of the audio.

            timetable (list[dict]):
                The timetable of the spoken words, as returned by the gentle interface.
        """

        # Object attributes
        self.transcript = transcript
        # self.transcript = transcript
        self.timetable = timetable
        self.duration = int(ceil(timetable[-1]["end"]))  # Get the time that the last word was spoken

    # Methods
    def align_time(self, block_duration=5):
        """
        Method that aligns the transcript by time.

        Args:
            block_duration (float):
                The length of time that makes up each block.
                Every block will have its own transcript section.
                (Default = 5)

        Returns:
            list[dict]:
                The aligned text dictionary.

        Raises:
            AssertionError:
                - If the value of `block_duration` is less than 3.
                - If `self.duration` is less than or equal to `block_duration`.
        """

        # Assert that the value of `block_duration` is valid
        assert block_duration >= 3, "The value of `block_duration` must be more than 3."
        assert self.duration > block_duration, "The length of the audio file is less than the block " \
                                               f"duration {block_duration}."

        # Calculate the number of blocks
        num_blocks = int(ceil(self.duration / block_duration))

        # Count the total number of processed words
        num_processed_words = len(self.timetable)  # Of course, some of the words may not have been processed

        # Start creating the aligned transcript
        aligned_words = []
        curr_processed_word_index = 0  # Stores the current processed word index

        for block_num in range(num_blocks):
            # Get as many words as possible before exceeding the block
            start_processed_word_index = curr_processed_word_index

            while curr_processed_word_index < num_processed_words:
                # Get the current word
                curr_word = self.timetable[curr_processed_word_index]

                # Check if the ending of that word is still in the block
                if "end" in curr_word and curr_word["end"] > (block_num + 1) * block_duration:
                    # The ending exceeded the block => the block has ended, so break
                    break

                # The word is still in the block, append to the list of block words
                curr_processed_word_index += 1

            # Get the index of the last processed word inside the block
            end_processed_word_index = curr_processed_word_index - 1  # The current word is not in the block

            # Get the processed words that are attributed to those two indices
            start_processed_word = self.timetable[start_processed_word_index]
            end_processed_word = self.timetable[end_processed_word_index]

            # Find all the words that are in between those two words
            words = self.transcript[start_processed_word["startOffset"]:end_processed_word["endOffset"] + 1].strip()

            # Clean up the words
            words = re.sub(r"\s+", " ", words.replace("\n", " "))  # Replace newlines with a single space

            # Add more info to the words
            dict_with_more_info = {
                "start_time": block_num * block_duration,
                "end_time": (block_num + 1) * block_duration,
                "text": words
            }

            # Append that dictionary to the `aligned_words` list
            aligned_words.append(dict_with_more_info)

        # Return the `aligned_words` list
        return aligned_words

    def align_sentence(self):
        """
        Method that aligns the transcript by sentence.

        Returns:
            list[dict]:
                The aligned text dictionary.
        """

        # Todo: fill in


# TESTING CODE
if __name__ == "__main__":
    # Imports
    import ast
    from pprint import pprint

    # Read the timetable and transcript
    aTranscript = open("../../TranscriptClean.txt", "r").read()
    aTimetable = ast.literal_eval(open("TestResponse.json", "r").read())

    # Create an `Aligner` object
    aligner = Aligner(aTranscript, aTimetable)

    # Align the words
    alignedWords = aligner.align_time()
    pprint(alignedWords)
