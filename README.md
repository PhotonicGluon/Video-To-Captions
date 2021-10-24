# Video-To-Captions

A Program that helps convert a media file and a transcript into a captions file with timestamps.

## Longer Description

This program aims to help cut down time on creating captions for videos which have a fixed transcript.

Creating captions for videos is sometimes a long and laborious process, so I've made this program to help relieve some
pain from the video creator.

Sometimes, you just have a static visual for your video, and it is the audio file which contains the audio data. This
program also supports this by including an "audio only" option.

## Requirements

- FFmpeg (install it using your system's package manager, **not using PIP**)
- [Docker](https://www.docker.com/) (you need this to install the [Gentle](https://github.com/lowerquality/gentle)
  docker container)
- Python 3.7+

## Installation Process

### Installing FFmpeg

#### For Windows

Go [here](https://www.ffmpeg.org/download.html#build-windows) and follow the instructions in the FFmpeg installer.

#### For Macintosh

1. Install [Homebrew](https://brew.sh/).
2. Run `brew install ffmpeg`.

#### For Ubuntu

Run

```bash
sudo apt install ffmpeg
```

### Installing [Gentle](https://github.com/lowerquality/gentle)

You will first need to install [Docker](https://www.docker.com/) on your machine.

Once you have installed it, run the following lines of code:

```bash
docker run --privileged -dp 8765:8765 --name gentle-container lowerquality/gentle
docker stop gentle-container
```

Wait for everything to be run. Now Gentle has been installed.

### Installing Everything Else

It is recommended to install the Python packages into a
[virtual environment](https://docs.python.org/3/tutorial/venv.html) to avoid clashes with your system's default Python
installation.

1. Open up a command line interface and navigate to the directory containing this document.
2. Assuming that you **only** have Python 3.7+, run `python -m pip install -r requirements.txt` to install all the
   necessary libraries.
3. Once it has installed everything, you are ready.

## Usage

To use the program, navigate to the root directory of the project and run

```bash
python main.py [video_or_audio_file] [transcript_file]
```

to generate a WebVTT captions file given the provided `video_or_audio_file` path and the `transcript_file` path.

You can customise the options to the program. Simply run

```bash
python main.py -h
```

to see all the available options that can be used.

## Supported Captioning Processes

The following list shows the currently accepted captioning processes:

- By `time`.
    - When captioning by time, words that belong within the same time interval will be placed in the same caption
      *block*, regardless of how long the block is.
    - This process ignores the sentence splits and only focuses on the words which make up the sentences.
- By `sentence`.
    - When captioning by sentence, each caption block will contain one sentence or `MAX_BLOCK_LENGTH` words, whichever
      is fewer.
    - Words that are in the same sentence will be grouped together in the same caption block and will be displayed
      together, unless the sentence has more than `MAX_BLOCK_LENGTH` words which the program will then split the
      sentence into multiple blocks.

## Supported Caption Formats

The following list shows the currently supported caption formats:

- Web Video Text Tracks format (WebVTT) [`.vtt`]
- SubRip Text (SubRip) [`.srt`]
