# Video Joiner with Fade Transitions

A Python script that joins multiple video files with smooth fade black transitions using FFmpeg.

## Features

- **Auto-detection**: Finds all `video*.mp4` files in the current directory
- **Standardization**: Converts all videos to the same resolution, fps, and codec
- **Smooth Transitions**: Adds fade black transitions between videos (0.2s duration)
- **Audio Crossfading**: Smooth audio transitions to match video fades
- **High Quality**: Uses H.264 with CRF 18 and slow preset for best quality

## Requirements

- FFmpeg with libx264 and aac support
- Python 3.6+

## Usage

1. Place your video files in this directory with names like:
   - `video1.mp4`
   - `video2.mp4` 
   - `video3.mp4`
   - etc.

2. Run the script:
   ```bash
   python video_joiner.py
   ```

3. The output will be saved as `output.mp4`

## Configuration

You can modify these settings in the script:

```python
# Video Settings
TARGET_WIDTH = 848
TARGET_HEIGHT = 478
TARGET_FPS = 24
CRF = 18                    # Quality (lower = better)
PRESET = "slow"             # Encoding speed vs quality

# Transition Settings
TRANSITION_DURATION = 0.2   # Seconds
TRANSITION_TYPE = "fadeblack"
```

## How it Works

1. **Standardization**: All input videos are converted to the same format
2. **Sequential Joining**: Videos are joined one by one with transitions
3. **Cleanup**: Temporary files are automatically removed

The script uses FFmpeg's `xfade` filter for video transitions and `acrossfade` for audio.