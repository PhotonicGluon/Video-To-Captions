"""
main.py

Created on 2021-05-03
Updated on 2021-05-03

Copyright © Ryan Kan

Description: The main file.
"""

# IMPORTS
import argparse
import os

from src.conversion import video_to_wav, timetable_to_webvtt
from src.gentle_interface import get_timetable
from src.timetable_fixing import Aligner

# CONSTANTS
CAPTION_TYPE_TO_EXTENSION = {
    "webvtt": ".vtt"
}

# INPUT
# Initialise the argument parser
parser = argparse.ArgumentParser(description="A Program that helps convert a video into a transcript with timestamps.")

# Add the arguments
parser.add_argument("video_file", help="The video file to be captioned.")
parser.add_argument("transcript_file", help="The transcript of the video.")

parser.add_argument("-b", "--block-type", help="How the captions should be grouped.", choices=["time"], default="time")
parser.add_argument("-c", "--caption-type", help="Format of the captions.", choices=["webvtt"], default="webvtt")
parser.add_argument("-o", "--output-file", help="Name of the output file, without the extension", default="transcript")

# Parse the arguments
args = parser.parse_args()

# Run validation on the provided inputs
if not os.path.isfile(args.video_file):
    raise FileNotFoundError(f"A video file does not exist at the path '{args.video_file}'.")

if not os.path.isfile(args.transcript_file):
    raise FileNotFoundError(f"A transcript does not exist at the path '{args.transcript}'.")

# PROCESSES
# Extract the audio from the video file
print("Extracting audio from video file...")
audioFilePath = video_to_wav(args.video_file, wav_file_name="audio_temp")

# Get the timetable from the audio file and the transcript
print("Getting timetable from transcript and audio file...")
alignedTimetable = get_timetable(audioFilePath, args.transcript_file)

# Align the timetable with the transcript
print("Aligning timetable with transcript...")
aligner = Aligner(open(args.transcript_file, "r").read(), alignedTimetable)

if args.block_type == "time":
    alignedTimetable = aligner.align_time()
else:
    alignedTimetable = None

# Convert the `alignedTimetable` into a captions string
print("Converting aligned timetable to captions...")
if args.caption_type == "webvtt":
    captionContent = timetable_to_webvtt(alignedTimetable)
else:
    captionContent = ""

# OUTPUT
print("Writing captions to file...")
with open(args.output_file + CAPTION_TYPE_TO_EXTENSION[args.caption_type], "w+") as f:
    f.write(captionContent)

print("Done!")

# CLEANUP
os.remove("audio_temp.wav")
