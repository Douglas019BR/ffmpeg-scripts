# Add Dual Audio to Video

A Python script that combines a video with two audio tracks in sequence. The OGG audio plays first, followed immediately by the MP3 audio, creating a seamless dual audio experience.

## Features

- **Automatic File Detection**: Finds video (`video*.mp4`), OGG audio (`*.ogg`), and MP3 audio (`*.mp3`) files in the current directory
- **Sequential Audio Playback**: OGG plays from start, MP3 begins after OGG ends
- **Duration Matching**: Both audio tracks are padded to match video duration
- **Audio Mixing**: Creates a single mixed audio track with proper timing
- **High Quality Output**: AAC encoding at 192k bitrate

## Requirements

- FFmpeg with ffprobe
- Python 3.6+

## Usage

1. Place your files in this directory:
   - `video*.mp4` (video file starting with "video")
   - `*.ogg` (first audio track)
   - `*.mp3` (second audio track)

2. Run the script:
   ```bash
   python add_audio.py
   ```

3. The output will be saved as `output.mp4`

## How it Works

1. **File Discovery**: Automatically detects required video and audio files
2. **Duration Analysis**: Measures duration of all input files using ffprobe
3. **Audio Track Creation**: 
   - Track 1: OGG audio padded to video duration
   - Track 2: MP3 audio delayed by OGG duration, then padded to video duration
4. **Mixing**: Both tracks are mixed together using FFmpeg's amix filter
5. **Final Output**: Video with mixed audio track, trimmed to video duration

## Audio Timeline

```
Video:    |---------------------------|
OGG:      |--------|.................|
MP3:      |........|-----------------|
Result:   |--------|-----------------|
```

The script uses FFmpeg's `filter_complex` with `apad`, `adelay`, and `amix` filters for precise audio timing and mixing.
