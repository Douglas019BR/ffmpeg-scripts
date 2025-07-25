# FFmpeg Scripts

A collection of utility scripts for audio and video editing using FFmpeg on Linux.

## Scripts

### add_dual_audio/
Combines a video with dual audio tracks in sequence. The OGG audio plays first, followed by MP3 audio.

### join_videos/
Joins multiple video files together (removes audio for compatibility). Handles different resolutions and codecs.

### join_videos_with_shadow_effect/
Joins multiple video files with smooth fade black transitions between them.

### accelerate_video/
Speeds up video files by a configurable rate (default 2.0x) while maintaining audio sync.

## Requirements

- FFmpeg (with libx264 and aac support)
- Python 3.6+

## Installation

1. Install FFmpeg:
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/Douglas019BR/ffmpeg-scripts.git
   cd ffmpeg-scripts
   ```

## Usage Pattern

Each script directory contains:
- Main Python script
- Detailed README with specific usage instructions
- Place required files in the script directory and run

## License

MIT License - see [LICENSE](LICENSE) for details.
