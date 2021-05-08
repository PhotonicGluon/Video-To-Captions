"""
transcript_aligner.py

Created on 2021-05-02
Updated on 2021-05-08

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

    def align_sentence(self, max_block_length=15):
        """
        Method that aligns the transcript by sentence.

        Args:
            max_block_length (int):
                The maximum number of timetabled words that can be in each caption block.
                This value must be a positive integer.
                (Default = 15)

        Returns:
            list[dict]:
                The aligned text dictionary.

        Notes:
            - A sentence is defined to be a string of text that ends with a punctuation mark (".", "?" and "!" only).
        """

        # Define sentence ending characters
        sentence_ending_characters = [".", "!", "?"]

        # Iterate through every timetable word
        aligned_words = []  # Stores the sentences with the start and end times
        block_start_time = None  # The starting time of the current caption block
        block_end_time = None  # The ending time of the current caption block
        block_start_index = None  # The starting index of the current caption block
        block_length = 0  # Stores the length of the current caption block
        start_of_sentence = True  # Whether the current word is the start of a new sentence

        for timetable_word in self.timetable:
            # Update the block's starting time & starting index, if needed
            if block_start_time is None:
                # Set the block's starting index
                block_start_index = timetable_word["startOffset"]

                # Check if the current word has a "start" key
                if "start" in timetable_word:
                    block_start_time = timetable_word["start"]
                else:
                    # Use the end time of the previous block instead
                    block_start_time = block_end_time

                # Update the `start_of_sentence` variable
                start_of_sentence = True

            # Find the starting and ending character's position
            start_pos = timetable_word["startOffset"]
            end_pos = timetable_word["endOffset"]  # This is the position of the character that is one after the word

            # Check if the sentence ends on the current word
            if self.transcript[end_pos] in sentence_ending_characters:
                # Set the time which the current caption block ends
                if "end" in timetable_word:
                    block_end_time = timetable_word["end"]
                else:
                    # Extrapolate the time based off the speed of reading
                    second_per_char = block_start_time / block_start_index  # Speed of reading each character
                    block_end_time = second_per_char * end_pos

                # Create the dictionary that will go into the `aligned_words` array
                dict_with_more_info = {
                    "start_time": block_start_time,
                    "end_time": block_end_time,
                    "text": self.transcript[block_start_index:end_pos + 1].strip()
                }

                aligned_words.append(dict_with_more_info)

                # Update the block's starting time, starting index and block length
                block_start_time = None  # Wait for the new word to override this
                block_start_index = None  # Wait for the new word to override this
                block_length = 0

            # Check if this is the start of a new sentence
            elif start_of_sentence:
                # Ignore and move on
                pass

            # Check if the sentence ended on the previous word
            else:
                # Get the non-whitespace character that is to the left of the word
                non_whitespace_char_pos = start_pos - 1

                while self.transcript[non_whitespace_char_pos].isspace():
                    non_whitespace_char_pos -= 1

                # Check if that character is one of the sentence ending characters
                if self.transcript[non_whitespace_char_pos] in sentence_ending_characters:
                    # Set the time which the current caption block ends
                    if "start" in timetable_word:
                        block_end_time = timetable_word["start"]  # We don't have the previous word's end time
                    else:
                        # Extrapolate the time based off the speed of reading
                        second_per_char = block_start_time / block_start_index  # Speed of reading each character
                        block_end_time = second_per_char * non_whitespace_char_pos

                    # Create the dictionary that will go into the `aligned_words` array
                    dict_with_more_info = {
                        "start_time": block_start_time,
                        "end_time": block_end_time,
                        "text": self.transcript[block_start_index:non_whitespace_char_pos + 1].strip()
                    }

                    aligned_words.append(dict_with_more_info)

                    # Update the block's starting time, starting index and block length
                    block_start_time = block_end_time  # The sentence already started
                    block_start_index = timetable_word["startOffset"]
                    block_length = 1  # We already have one word

                # Check if the `block_length` has exceeded or equals the `max_block_length`
                elif block_length >= max_block_length:
                    # Set the time which the current caption block ends
                    if "start" in timetable_word:
                        block_end_time = timetable_word["end"]
                    else:
                        # Extrapolate the time based off the speed of reading
                        second_per_char = block_start_time / block_start_index  # Speed of reading each character
                        block_end_time = second_per_char * end_pos

                    # Create the dictionary that will go into the `aligned_words` array
                    dict_with_more_info = {
                        "start_time": block_start_time,
                        "end_time": block_end_time,
                        "text": self.transcript[block_start_index:end_pos + 1].strip()
                    }

                    aligned_words.append(dict_with_more_info)

                    # Update the block's starting time
                    block_start_time = block_end_time  # Continue the sentence in the next block
                    block_start_index = end_pos + 1  # Exclude the space before the word
                    block_length = 0  # Reset the length of each block back to 0

            # Update the value of `start_of_sentence` and `block_length`
            start_of_sentence = False
            block_length += 1  # Added one more timetabled word

        # Return the `aligned_words` array
        return aligned_words

        # # Todo: re-write this part, but use the timetable words as reference points instead of the raw transcript.
        # #       This is because the timetable words cannot be wrong and will definitely appear in the transcript. But
        # #       the words that we independently extract here may not be correct and may cause weird errors.
        #
        # # Get all the sentences in the transcript
        # plain_text = re.sub(r"\s+", " ", self.transcript.replace("\n", " ")).lstrip()
        # sentences = re.split(r"[.!?-]", plain_text)
        # print(sentences)
        #
        # # Iterate through each sentence and attempt to determine the time which the sentence started and when it ended
        # aligned_words = []
        # current_timetabled_word_index = 0
        #
        # for sentence in sentences:
        #     # Split each sentence with the space being the delimiter
        #     pseudo_words = sentence.split()  # It may not a word per se, but it is close enough for a comparison
        #
        #     # Count the number of pseudo-words
        #     num_pseudo_words = len(pseudo_words)
        #
        #     # Count the number of blocks that are needed to complete the sentence
        #     num_blocks = int(ceil(num_pseudo_words / max_block_length))
        #
        #     # Get the start and end time of the blocks in the sentence
        #     for block_num in range(num_blocks):
        #         # Get the start and end word of the block
        #         start_word = self.timetable[current_timetabled_word_index]
        #
        #         for pseudo_word in pseudo_words[block_num * max_block_length:(block_num + 1) * max_block_length]:
        #             # print("PSEUDO-WORD", pseudo_word, self.timetable[current_timetabled_word_index]) todo: remove
        #             # Check if the pseudo-word is found inside the timetable
        #             current_timetable_word = self.timetable[current_timetabled_word_index]
        #             if pseudo_word.lower().find(current_timetable_word["word"].lower()) != -1:
        #                 current_timetabled_word_index += 1  # Increment the timetabled word index
        #
        #         end_word = self.timetable[current_timetabled_word_index]
        #
        #         # Check if the end word is valid
        #         while end_word["case"] != "success":
        #             current_timetabled_word_index += 1
        #             end_word = self.timetable[current_timetabled_word_index]
        #
        #         # Process the text that will be in the block
        #         raw_block_text = self.transcript[start_word["startOffset"]:end_word["startOffset"]]
        #
        #         # Remove the last character as it is a space
        #         raw_block_text = raw_block_text[:-1]
        #
        #         # Remove all newline characters
        #         block_text = re.sub(r"\s+", " ", raw_block_text.replace("\n", " "))
        #         print(f"'{block_text}'", start_word, end_word)
        #
        #         # Convert that info to a dictionary
        #         dict_with_more_info = {
        #             "start_time": start_word["start"],
        #             "end_time": end_word["start"],
        #             "text": block_text
        #         }
        #
        #         # Append that dictionary to the `aligned_words` array
        #         aligned_words.append(dict_with_more_info)
        #
        # # Return the aligned words array
        # return aligned_words


# TESTING CODE
if __name__ == "__main__":
    # Imports
    import ast

    # Read the timetable and transcript
    aTranscript = open("../../TranscriptClean.txt", "r").read()
    aTimetable = ast.literal_eval(open("TestResponse.txt", "r").read())

    # Create an `Aligner` object
    aligner = Aligner(aTranscript, aTimetable)

    # Align the words
    alignedWords = aligner.align_sentence()
    print(alignedWords)
