"""
timetable_to_subrip.py

Created on 2021-05-15
Updated on 2021-05-15

Copyright © Ryan Kan

Description: Converts the aligned timetable into the SubRip format.

References:
    - https://en.wikipedia.org/wiki/SubRip#SubRip_text_file_format
"""

# IMPORTS
from datetime import timedelta


# FUNCTIONS
def timedelta_to_subrip_time(timedelta_object):
    """
    Converts a timedelta object to a valid SubRip timestamp.

    Args:
        timedelta_object (datetime.timedelta)

    Returns:
        str
    """

    # Create an auxiliary timedelta object without any microseconds
    auxiliary_timedelta = timedelta(seconds=timedelta_object.seconds)

    # Get the auxiliary timedelta's string representation
    final = str(auxiliary_timedelta)  # Should be in the form "HH:MM:SS"

    # Now add on the milliseconds
    final += f",{timedelta_object.microseconds // 1000:03d}"  # Should now be in the form "HH:MM:SS,mmm"

    # Return the final string
    return final


def timetable_to_subrip(aligned_timetable):
    """
    Converts the aligned timetable into the SubRip format.

    Args:
        aligned_timetable (list[dict]):
            An aligned timetable that is output by the `Aligner` class.

    Returns:
        str:
            Text representing a SubRip file.
    """

    # Define a variable to contain the file's contents
    file_contents = ""

    # Process each block
    for i, block in enumerate(aligned_timetable):
        # Define a temporary variable to store this caption block
        block_text = f"{i + 1}\n"  # Every SubRip caption block starts with a number

        # Get the start and end time of the block
        start_time = timedelta_to_subrip_time(timedelta(seconds=block["start_time"]))
        end_time = timedelta_to_subrip_time(timedelta(seconds=block["end_time"]))

        # Add the timing line to the block of text
        block_text += f"{start_time} --> {end_time}\n"

        # Add the line of text from the `block` to the block of text
        block_text += block["text"] + "\n\n"

        # Add the `block_text` to the `file_contents`
        file_contents += block_text

    # Return the final file's contents
    return file_contents


# TESTING CODE
if __name__ == "__main__":
    # Imports
    import ast

    # Read the aligned timetable from the test file
    alignedTimetable = ast.literal_eval(open("AlignedTimetable.txt", "r").read())

    # Test the conversion function
    subrip = timetable_to_subrip(alignedTimetable)
    print(subrip)
