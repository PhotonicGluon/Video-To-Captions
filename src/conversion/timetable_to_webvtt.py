"""
timetable_to_webvtt.py

Created on 2021-05-02
Updated on 2021-05-02

Copyright © Ryan Kan

Description: Converts the aligned timetable into the WebVTT format.
"""


# FUNCTIONS
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

        # Get the hour, minute and second of the start time
        hour = block["start_time"] // 3600
        minute = (block["start_time"] - hour * 3600) // 60
        second = block["start_time"] - hour * 3600 - minute * 60
        start_time = f"{hour:02d}:{minute:02d}:{second:02d}.000"

        # Get the hour, minute and second of the end time
        hour = block["end_time"] // 3600
        minute = (block["end_time"] - hour * 3600) // 60
        second = block["end_time"] - hour * 3600 - minute * 60
        end_time = f"{hour:02d}:{minute:02d}:{second:02d}.000"

        # Add the timing line to the block of text
        block_text += f"{start_time} --> {end_time}\n"

        # Add the line of text to the block of text
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
