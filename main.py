"""
main.py

Created on 2021-05-03
Updated on 2021-05-11

Copyright © Ryan Kan

Description: The main file.

Todo:
    - Make this work for just audio files with no video.
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

parser.add_argument("-b", "--block-type", choices=["time", "sentence"], default="sentence",
                    help="How the captions should be grouped.")
parser.add_argument("-d", "--block-duration", type=int, default=5,
                    help="The length of time that makes up each block. Must be a positive integer."
                         "Provide it only if `block-type` is 'time'.")
parser.add_argument("-l", "--max-block-length", type=int, default=15,
                    help="The maximum number of timetabled words that can be in each caption block. Must be a "
                         "positive integer. Provide it only if `block-type` is 'sentence'.")
parser.add_argument("-c", "--caption-type", choices=["webvtt"], default="webvtt", help="Format of the captions.")
parser.add_argument("-o", "--output-file-name", default="transcript",
                    help="Name of the output file, without the extension.")

# Parse the arguments
args = parser.parse_args()

# Run validation on the provided inputs
if not os.path.isfile(args.video_file):
    raise FileNotFoundError(f"A video file does not exist at the path '{args.video_file}'.")

if not os.path.isfile(args.transcript_file):
    raise FileNotFoundError(f"A transcript does not exist at the path '{args.transcript}'.")

assert args.block_duration > 0, "The block duration must be a positive integer."
assert args.max_block_length > 0, "The maximum block length must be a positive integer."

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
    alignedTimetable = aligner.align_time(args.block_duration)
elif args.block_type == "sentence":
    alignedTimetable = aligner.align_sentence(args.max_block_length)

# Convert the `alignedTimetable` into a captions string
print("Converting aligned timetable to captions...")
if args.caption_type == "webvtt":
    captionContent = timetable_to_webvtt(alignedTimetable)
else:
    captionContent = ""

# OUTPUT
print("Writing captions to file...")
with open(args.output_file_name + CAPTION_TYPE_TO_EXTENSION[args.caption_type], "w+") as f:
    f.write(captionContent)

print("Done!\nPlease review the generated file and fix any errors that may arise during captioning.")

# CLEANUP
# Remove the temporary audio file
os.remove("audio_temp.wav")
