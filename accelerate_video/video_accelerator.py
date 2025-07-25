
import subprocess
import os
import sys

def get_input_filename():
    for f in os.listdir('.'):
        if f.startswith('video') and f.endswith('.mp4'):
            return f
    return None

def run_ffmpeg_command(command, description):
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running ffmpeg for: {description}", file=sys.stderr)
        print(f"FFMPEG STDERR: {e.stderr}", file=sys.stderr)
        return False

def main():
    input_video = get_input_filename()
    if not input_video:
        print("No video file found starting with 'video' and ending with '.mp4'", file=sys.stderr)
        sys.exit(1)

    output_video = "output.mp4"
    acceleration_rate = 2.0

    if os.path.exists(output_video):
        os.remove(output_video)

    command = [
        "ffmpeg",
        "-i", input_video,
        "-vf", f"setpts={1/acceleration_rate}*PTS",
        "-af", f"atempo={acceleration_rate}",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-y", output_video
    ]

    if not run_ffmpeg_command(command, f"Accelerating {input_video}"):
        sys.exit(1)

    print(f"Video accelerated successfully! Output saved to {output_video}")

if __name__ == "__main__":
    main()
