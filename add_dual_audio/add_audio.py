import subprocess
import os
import sys
import shutil


def get_input_files():
    video = None
    ogg_audio = None
    mp3_audio = None
    for f in os.listdir("."):
        if f.startswith("video") and f.endswith(".mp4"):
            video = f
        elif f.endswith(".ogg"):
            ogg_audio = f
        elif f.endswith(".mp3"):
            mp3_audio = f
    return video, ogg_audio, mp3_audio


def get_duration(filename):
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        filename,
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"Error getting duration for {filename}: {e}", file=sys.stderr)
        return None


def run_ffmpeg_command(command, description):
    print(f"\nRunning: {description}")
    print(
        "Command: " + " ".join(f"'{part}'" if " " in part else part for part in command)
    )
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError running ffmpeg for: {description}", file=sys.stderr)
        print(f"FFMPEG STDERR:\n{e.stderr}", file=sys.stderr)
        return False


def main():
    video, ogg_audio, mp3_audio = get_input_files()
    if not all([video, ogg_audio, mp3_audio]):
        print(
            "Missing one or more input files (video.mp4, audio.ogg, audio.mp3)",
            file=sys.stderr,
        )
        sys.exit(1)

    output_file = "output.mp4"
    temp_dir = "temp_audio"

    if os.path.exists(output_file):
        os.remove(output_file)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    video_duration = get_duration(video)
    ogg_duration = get_duration(ogg_audio)
    mp3_duration = get_duration(mp3_audio)

    if video_duration is None or ogg_duration is None or mp3_duration is None:
        print("Error: Could not get duration for one or more files", file=sys.stderr)
        sys.exit(1)

    print(f"Video duration: {video_duration:.2f}s")
    print(f"OGG duration: {ogg_duration:.2f}s")
    print(f"MP3 duration: {mp3_duration:.2f}s")

    # Create final audio tracks using filter_complex (direct approach)
    # Track 1: OGG audio padded to video duration
    # Track 2: MP3 audio delayed by OGG duration, then padded to video duration

    cmd_final = [
        "ffmpeg",
        "-i",
        video,
        "-i",
        ogg_audio,
        "-i",
        mp3_audio,
        "-filter_complex",
        f"[1:a]apad=whole_dur={video_duration}[ogg_track];"
        f"[2:a]adelay={int(ogg_duration * 1000)}|{int(ogg_duration * 1000)},apad=whole_dur={video_duration}[mp3_track];"
        f"[ogg_track][mp3_track]amix=inputs=2:duration=first[final_audio]",
        "-map",
        "0:v",
        "-map",
        "[final_audio]",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        str(video_duration),
        output_file,
    ]

    if not run_ffmpeg_command(cmd_final, "Creating final video with dual audio"):
        sys.exit(1)

    # Clean up temp directory
    shutil.rmtree(temp_dir)
    print(f"\nAudio added successfully! Output saved to {output_file}")


if __name__ == "__main__":
    main()
