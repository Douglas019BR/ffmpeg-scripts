# Video Accelerator

A Python script to accelerate a video file using FFmpeg.

## Features

- **Auto-detection**: Finds a `video*.mp4` file in the current directory.
- **Acceleration**: Speeds up the video and audio by a 2.0x rate.
- **High Quality**: Uses H.264 with CRF 18 and slow preset for good quality.

## Requirements

- FFmpeg with libx264 and aac support
- Python 3.6+

## Usage

1. Place your video file in this directory with a name like:
   - `video.mp4`
   - `video1.mp4`

2. Run the script:
   ```bash
   python video_accelerator.py
   ```

3. The output will be saved as `output.mp4`

## Configuration

You can modify these settings in the script:

```python
# Acceleration Rate
acceleration_rate = 2.0
```

## How it Works

The script uses FFmpeg's `setpts` filter for video and `atempo` filter for audio to achieve the acceleration effect.
