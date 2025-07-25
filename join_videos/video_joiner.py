import subprocess
import os
import sys
import re


def get_video_files():
    def extract_number(filename):
        match = re.search(r"video(\d+)\.mp4$", filename)
        return int(match.group(1)) if match else float("inf")

    return sorted(
        [f for f in os.listdir(".") if f.startswith("video") and f.endswith(".mp4")],
        key=extract_number,
    )


def run_ffmpeg_command(command, description):
    print(f"\nRunning: {description}")
    print(
        "Command: " + " ".join(f"'{part}'" if " " in part else part for part in command)
    )
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError running ffmpeg for: {description}", file=sys.stderr)
        print(f"FFMPEG STDERR:\n{e.stderr}", file=sys.stderr)
        return False


def get_video_info(filename):
    """Get video information using ffprobe"""
    try:
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            filename,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json

        data = json.loads(result.stdout)

        video_stream = None
        audio_stream = None

        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video" and not video_stream:
                video_stream = stream
            elif stream.get("codec_type") == "audio" and not audio_stream:
                audio_stream = stream

        return {
            "video_codec": video_stream.get("codec_name") if video_stream else None,
            "audio_codec": audio_stream.get("codec_name") if audio_stream else None,
            "width": video_stream.get("width") if video_stream else None,
            "height": video_stream.get("height") if video_stream else None,
            "fps": eval(video_stream.get("r_frame_rate", "0/1"))
            if video_stream
            else None,
        }
    except Exception as e:
        print(f"Warning: Could not get info for {filename}: {e}")
        return None


def videos_are_compatible(video_files):
    """Check if videos have compatible formats for direct concatenation"""
    if not video_files:
        return True

    first_info = get_video_info(video_files[0])
    if not first_info:
        return False

    for video_file in video_files[1:]:
        info = get_video_info(video_file)
        if not info:
            return False

        # Check if key parameters match (ignoring audio since we'll remove it)
        if (
            info["video_codec"] != first_info["video_codec"]
            or info["width"] != first_info["width"]
            or info["height"] != first_info["height"]
        ):
            return False

    return True


def main():
    video_files = get_video_files()
    if not video_files:
        print(
            "No video files found starting with 'video' and ending with '.mp4'",
            file=sys.stderr,
        )
        sys.exit(1)

    output_file = "output.mp4"
    concat_file_path = "concat_list.txt"

    # Remove output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    print(f"Found {len(video_files)} videos: {', '.join(video_files)}")
    print("Checking video compatibility...")

    # Check if videos are compatible for direct concatenation
    compatible = videos_are_compatible(video_files)

    if compatible:
        print("Videos are compatible - using fast concatenation (no audio)")

        # Create concat file with list of videos
        with open(concat_file_path, "w") as f:
            for filename in video_files:
                # Use absolute path to avoid issues
                abs_path = os.path.abspath(filename)
                f.write(f"file '{abs_path}'\n")

        # Concatenate videos without re-encoding and without audio
        join_cmd = [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_file_path,
            "-c:v",
            "copy",  # Copy video stream without re-encoding
            "-an",  # No audio
            "-y",
            output_file,
        ]

        success = run_ffmpeg_command(join_cmd, "Joining videos (no audio)")

    else:
        print(
            "Videos have different formats - using filter_complex for proper concatenation"
        )

        # Build input arguments
        input_args = []
        filter_parts = []

        for i, filename in enumerate(video_files):
            input_args.extend(["-i", filename])
            # Scale all videos to a common resolution and remove audio
            filter_parts.append(
                f"[{i}:v]scale=848:478:force_original_aspect_ratio=decrease,pad=848:478:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}];"
            )

        # Create filter_complex argument - concatenate only video streams
        filter_complex = (
            "".join(filter_parts)
            + "".join([f"[v{i}]" for i in range(len(video_files))])
            + f"concat=n={len(video_files)}:v=1:a=0[outv]"
        )

        join_cmd = (
            ["ffmpeg"]
            + input_args
            + [
                "-filter_complex",
                filter_complex,
                "-map",
                "[outv]",
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "23",
                "-an",  # No audio
                "-y",
                output_file,
            ]
        )

        success = run_ffmpeg_command(join_cmd, "Joining videos with scaling (no audio)")

    # Clean up concat file if it exists
    if os.path.exists(concat_file_path):
        os.remove(concat_file_path)

    if success:
        print(f"\nVideos joined successfully! Output saved to {output_file}")
        print(f"Joined {len(video_files)} videos in order: {', '.join(video_files)}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
