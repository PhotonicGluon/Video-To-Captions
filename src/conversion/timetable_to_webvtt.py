"""
timetable_to_webvtt.py

Created on 2021-05-02
Updated on 2021-05-08

Copyright © Ryan Kan

Description: Converts the aligned timetable into the WebVTT format.
"""

# IMPORTS
from datetime import timedelta


# FUNCTIONS
def timedelta_to_webvtt_time(timedelta_object):
    """
    Converts a timedelta object to a valid WebVTT timestamp.

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
    final += f".{timedelta_object.microseconds // 1000:03d}"  # Should now be in the form "HH:MM:SS.mmm"

    # Return the final string
    return final


def timetable_to_webvtt(aligned_timetable):
    """
    Converts the aligned timetable into the WebVTT format.

    Args:
        aligned_timetable (list[dict]):
            An aligned timetable that is output by the Aligner class.

    Returns:
        str:
            Text representing a WebVTT file.
    """

    # Every WebVTT file starts with this
    file_contents = "WEBVTT\n\n"

    # Process each block
    for block in aligned_timetable:
        # Define a temporary variable to store this caption block
        block_text = ""

        # Get the start and end time of the block
        start_time = timedelta_to_webvtt_time(timedelta(seconds=block["start_time"]))
        end_time = timedelta_to_webvtt_time(timedelta(seconds=block["end_time"]))

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
    vtt = timetable_to_webvtt(alignedTimetable)
    print(vtt)
