# Video Joiner

A Python script that joins multiple video files intelligently, handling different formats and producing video-only output for maximum compatibility.

## Features

- **Auto-detection**: Finds all `video*.mp4` files in the current directory and sorts them numerically
- **Compatibility Check**: Analyzes video formats to choose optimal joining method
- **Smart Processing**: 
  - Fast concatenation for compatible videos (same codec, resolution)
  - Re-encoding with scaling for incompatible videos
- **Video-only Output**: Removes audio tracks to avoid sync issues and reduce file size
- **Quality Preservation**: Uses appropriate encoding settings based on input compatibility

## Requirements

- FFmpeg with libx264 support
- Python 3.6+

## Usage

1. Place your video files in this directory with names like:
   - `video1.mp4`
   - `video2.mp4`
   - `video3.mp4`

2. Run the script:
   ```bash
   python video_joiner.py
   ```

3. The output will be saved as `output.mp4` (video only, no audio)

## Processing Methods

### Compatible Videos (Fast Mode)
- Uses FFmpeg's concat demuxer
- Copies video stream without re-encoding
- Fastest processing, preserves original quality

### Incompatible Videos (Scaling Mode)
- Scales all videos to 848x478 resolution
- Uses filter_complex for proper concatenation
- Re-encodes with H.264, CRF 23, fast preset

## How it Works

1. **File Detection**: Scans directory for video files matching pattern
2. **Compatibility Analysis**: Checks codec, resolution, and dimensions using ffprobe
3. **Method Selection**: Chooses fast concat or scaling based on compatibility
4. **Processing**: Joins videos using selected method
5. **Cleanup**: Removes temporary files automatically

## Note

Audio is intentionally removed from the output to:
- Prevent audio sync issues between different source videos
- Reduce processing complexity and file size
- Ensure consistent output regardless of input audio formats
