"""
main.py

Created on 2021-05-03
Updated on 2021-05-15

Copyright © Ryan Kan

Description: The main file.
"""

# IMPORTS
import argparse
import os

from src.conversion import video_to_wav, audio_to_wav, timetable_to_subrip, timetable_to_webvtt, \
    SUPPORTED_VIDEO_EXTENSIONS, SUPPORTED_AUDIO_EXTENSIONS
from src.gentle_interface import get_timetable
from src.timetable_fixing import Aligner

# CONSTANTS
CAPTION_TYPE_TO_EXTENSION = {
    "webvtt": ".vtt",
    "subrip": ".srt"
}

# INPUT
# Initialise the argument parser
parser = argparse.ArgumentParser(description="A Program that helps convert a video into a transcript with timestamps.",
                                 formatter_class=argparse.RawTextHelpFormatter)

# Add the arguments
parser.add_argument("video_or_audio_file", help=f"The video/audio file to be captioned. The extension of the file "
                                                f"should be in one of the following lists:\n"
                                                f"Video: {list(SUPPORTED_VIDEO_EXTENSIONS.keys())}\n"
                                                f"Audio: {list(SUPPORTED_AUDIO_EXTENSIONS.keys())}")
parser.add_argument("transcript_file", help="The transcript of the video.")

parser.add_argument("-b", "--block-type", choices=["time", "sentence"], default="sentence",
                    help="How the captions should be grouped.")
parser.add_argument("-d", "--block-duration", type=int, default=5,
                    help="The length of time that makes up each block. Must be a positive integer."
                         "Provide it only if `block-type` is 'time'.")
parser.add_argument("-l", "--max-block-length", type=int, default=15,
                    help="The maximum number of timetabled words that can be in each caption block. Must be a "
                         "positive integer. Provide it only if `block-type` is 'sentence'.")
parser.add_argument("-c", "--caption-type", choices=["webvtt", "subrip"], default="webvtt",
                    help="Format of the captions.")
parser.add_argument("-o", "--output-file-name", default="transcript",
                    help="Name of the output file, without the extension.")

# Parse the arguments
args = parser.parse_args()

# Run validation on the provided inputs
if not os.path.isfile(args.video_or_audio_file):
    raise FileNotFoundError(f"A file does not exist at the path '{args.video_or_audio_file}'.")

if not os.path.isfile(args.transcript_file):
    raise FileNotFoundError(f"A transcript does not exist at the path '{args.transcript}'.")

assert args.block_duration > 0, "The block duration must be a positive integer."
assert args.max_block_length > 0, "The maximum block length must be a positive integer."

extension = os.path.splitext(args.video_or_audio_file)[-1]
assert extension in SUPPORTED_VIDEO_EXTENSIONS or extension in SUPPORTED_AUDIO_EXTENSIONS, \
    "The format of the video or audio file is not currently supported. " \
    f"(Supported: {list(SUPPORTED_VIDEO_EXTENSIONS.keys()) + list(SUPPORTED_AUDIO_EXTENSIONS.keys())}"

# PROCESSES
# Get the extension of the video or audio file
extension = os.path.splitext(args.video_or_audio_file)[-1]

# Extract the audio from the video or audio file depending on the file's extension
print("Extracting audio from the video or audio file...")
if extension in SUPPORTED_VIDEO_EXTENSIONS:
    audioFilePath = video_to_wav(args.video_or_audio_file, wav_file_name="audio_temp")
else:
    audioFilePath = audio_to_wav(args.video_or_audio_file, wav_file_name="audio_temp")

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
elif args.caption_type == "subrip":
    captionContent = timetable_to_subrip(alignedTimetable)
else:
    # This should never get here, but just in case include an else clause
    captionContent = ""

# OUTPUT
print("Writing captions to file...")
with open(args.output_file_name + CAPTION_TYPE_TO_EXTENSION[args.caption_type], "w+") as f:
    f.write(captionContent)

print("Done. Please review the generated file and fix any errors that may arise during captioning.")

# CLEANUP
# Remove the temporary audio file
os.remove("audio_temp.wav")
