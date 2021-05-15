# Video-To-Captions: Examples
This folder contains the example files that can be used when testing the program's functionality before trying it out with a bigger file.

## Usage
To test out the video to caption file process, navigate back to the root directory of the project and run
```bash
python main.py examples/lucier.mp4 examples/lucier.txt 
```

To test out the audio to caption file process, run
```bash
python main.py examples/lucier.mp3 examples/lucier.txt 
```
in the root directory of the project instead.

In both of the above examples, the file that is generated is in the WebVTT format. Thus its corresponding output is named `WebVTT.vtt`.

The output that is generated in the SubRip Text format is named `SubRip.srt`.
