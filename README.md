# Video-To-Captions
A Program that helps convert a video into a captions file with timestamps.

## Requirements
- FFmpeg (install it using your system's package manager, not using PIP)
- [Docker](https://www.docker.com/) (you need this to install [Gentle](https://github.com/lowerquality/gentle))
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
You will first need [Docker](https://www.docker.com/) installed.

Once you have installed it, run the following lines of code:
```bash
docker run --privileged -dp 8765:8765 --name gentle-container lowerquality/gentle
docker stop gentle-container
```

Wait for everything to be run. Now Gentle has been installed.

### Installing Everything Else
It is recommended to install the Python packages into a [virtual environment](https://docs.python.org/3/tutorial/venv.html).

1. Open up a command line interface and navigate to the directory containing this document.
2. Assuming that you **only** have Python 3.7+, run `python -m pip install -r requirements.txt`.
