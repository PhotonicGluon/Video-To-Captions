# Video-To-Transcript
A Program that helps convert a video into a transcript with timestamps

## Requirements
- ffmpeg (install it using your system's package manager, not using PIP)
- Docker (you need this to install Gentle)

## Installation Process
### Installing Gentle
Run the following lines of code:
```bash
docker run --privileged -dp 8765:8765 --name gentle-container lowerquality/gentle
docker stop gentle-container
```
