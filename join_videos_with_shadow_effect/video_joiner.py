

import subprocess
import os
import sys
import shutil
import re

# --- Configuration ---
def extract_number(filename):
    match = re.search(r'video(\d+)\.mp4$', filename)
    return int(match.group(1)) if match else float('inf')

VIDEO_FILES = sorted(
    [f for f in os.listdir('.') if f.startswith('video') and f.endswith('.mp4')],
    key=extract_number
)
TRANSITION_DURATION = 0.2
TRANSITION_TYPE = "fadeblack"
OUTPUT_FILE = "output.mp4"
TEMP_DIR = "temp_videos"
FINAL_TEMP_DIR = "temp_final"  # for intermediate join results

# --- Quality and Processing ---
TARGET_WIDTH = 848
TARGET_HEIGHT = 478
TARGET_FPS = 24
CRF = 18
PRESET = "slow"

def run_ffmpeg_command(command, description):
    """Runs an ffmpeg command and handles errors."""
    print(f"\nRunning: {description}")
    # Use a more shell-friendly way to show the command
    print("Command: " + " ".join(f"'{part}'" if " " in part else part for part in command))
    try:
        # Using PIPE to capture output, hiding it unless there's an error
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError running ffmpeg for: {description}", file=sys.stderr)
        print(f"FFMPEG STDERR:\n{e.stderr}", file=sys.stderr)
        return False

def get_duration(filename):
    """Gets the duration of a video file using ffprobe."""
    command = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", filename
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"Error getting duration for {filename}: {e.stderr}", file=sys.stderr)
        return None

def main():
    """Main function to generate the video."""
    # --- 1. Setup ---
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    if os.path.exists(FINAL_TEMP_DIR):
        shutil.rmtree(FINAL_TEMP_DIR)
    os.makedirs(TEMP_DIR)
    os.makedirs(FINAL_TEMP_DIR)

    # --- 2. Standardize all video files ---
    standardized_files = []
    for i, filename in enumerate(VIDEO_FILES):
        temp_filename = os.path.join(TEMP_DIR, f"temp_{i}.mp4")
        standardized_files.append(temp_filename)
        command = [
            "ffmpeg", "-i", filename,
            "-vf", f"scale={TARGET_WIDTH}:{TARGET_HEIGHT},fps={TARGET_FPS},setpts=PTS-STARTPTS",
            "-af", "asetpts=PTS-STARTPTS",
            "-c:v", "libx264", "-preset", PRESET, "-crf", str(CRF),
            "-c:a", "aac", "-b:a", "192k",
            "-y", temp_filename
        ]
        if not run_ffmpeg_command(command, f"Standardizing {filename}"):
            sys.exit(1)

    # --- 3. Join videos sequentially ---
    if not standardized_files:
        print("No video files found.", file=sys.stderr)
        sys.exit(1)

    current_video = standardized_files[0]

    for i in range(1, len(standardized_files)):
        next_video = standardized_files[i]
        output_join_path = os.path.join(FINAL_TEMP_DIR, f"join_{i - 1}.mp4")

        duration = get_duration(current_video)
        if duration is None:
            sys.exit(1)
        transition_offset = duration - TRANSITION_DURATION

        join_cmd = [
            "ffmpeg", "-i", current_video, "-i", next_video,
            "-filter_complex",
            f"[0:v][1:v]xfade=transition={TRANSITION_TYPE}:duration={TRANSITION_DURATION}:offset={transition_offset}[v];" +
            f"[0:a][1:a]acrossfade=d={TRANSITION_DURATION}[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", PRESET, "-crf", str(CRF),
            "-c:a", "aac", "-b:a", "192k",
            "-y", output_join_path
        ]

        if not run_ffmpeg_command(join_cmd, f"Joining step {i}/{len(standardized_files) - 1}"):
            sys.exit(1)

        current_video = output_join_path

    # --- 4. Finalize ---
    shutil.move(current_video, OUTPUT_FILE)

    # --- 5. Cleanup ---
    print("\nCleaning up temporary files...")
    shutil.rmtree(TEMP_DIR)
    shutil.rmtree(FINAL_TEMP_DIR)
    print("Done!")

if __name__ == "__main__":
    main()
