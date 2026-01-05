#!/usr/bin/env python3
"""
Video Converter using FFmpeg
Converts video files to different formats and resolutions
"""

import ffmpeg
import argparse
import sys
from pathlib import Path


def convert_video(input_file, output_file=None, output_format="mp4",
                 resolution=None, video_codec="libx264", audio_codec="aac",
                 video_bitrate=None, audio_bitrate="192k"):
    """
    Convert a video file to different format/resolution

    Args:
        input_file: Input video file path
        output_file: Output file path (auto-generated if None)
        output_format: Output format (mp4, webm, mkv, avi)
        resolution: Output resolution (e.g., "1920x1080", "1280x720")
        video_codec: Video codec (libx264, libx265, libvpx-vp9)
        audio_codec: Audio codec (aac, mp3, opus)
        video_bitrate: Video bitrate (e.g., "2M", "5M")
        audio_bitrate: Audio bitrate (default: 192k)
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        return False

    # Generate output filename if not provided
    if output_file is None:
        output_file = input_path.stem + f"_converted.{output_format}"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Converting: {input_file} -> {output_file}")

        # Build ffmpeg command
        stream = ffmpeg.input(input_file)

        # Apply video filters if resolution is specified
        if resolution:
            width, height = map(int, resolution.split('x'))
            stream = ffmpeg.filter(stream, 'scale', width, height)

        # Set output options
        output_options = {
            'vcodec': video_codec,
            'acodec': audio_codec,
            'audio_bitrate': audio_bitrate,
        }

        if video_bitrate:
            output_options['video_bitrate'] = video_bitrate

        # Run conversion
        stream = ffmpeg.output(stream, str(output_file), **output_options)
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)

        print(f"\nSuccessfully converted to: {output_file}")
        return True

    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error converting video: {e}", file=sys.stderr)
        return False


def extract_clip(input_file, output_file, start_time, duration=None, end_time=None):
    """
    Extract a clip from a video

    Args:
        input_file: Input video file path
        output_file: Output file path
        start_time: Start time (format: "HH:MM:SS" or seconds)
        duration: Duration in seconds (optional)
        end_time: End time (format: "HH:MM:SS" or seconds) (optional)
    """
    try:
        print(f"Extracting clip from: {input_file}")

        stream = ffmpeg.input(input_file, ss=start_time)

        output_options = {'c': 'copy'}  # Copy codec without re-encoding

        if duration:
            output_options['t'] = duration
        elif end_time:
            output_options['to'] = end_time

        stream = ffmpeg.output(stream, output_file, **output_options)
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)

        print(f"Successfully extracted clip to: {output_file}")
        return True

    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error extracting clip: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Convert videos using FFmpeg")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert video format/resolution')
    convert_parser.add_argument("input", help="Input video file")
    convert_parser.add_argument("-o", "--output", help="Output file path")
    convert_parser.add_argument("-f", "--format", default="mp4",
                               choices=["mp4", "webm", "mkv", "avi"],
                               help="Output format (default: mp4)")
    convert_parser.add_argument("-r", "--resolution",
                               help="Output resolution (e.g., 1920x1080, 1280x720)")
    convert_parser.add_argument("--vcodec", default="libx264",
                               help="Video codec (default: libx264)")
    convert_parser.add_argument("--acodec", default="aac",
                               help="Audio codec (default: aac)")
    convert_parser.add_argument("--vbitrate", help="Video bitrate (e.g., 2M)")
    convert_parser.add_argument("--abitrate", default="192k",
                               help="Audio bitrate (default: 192k)")

    # Clip command
    clip_parser = subparsers.add_parser('clip', help='Extract a clip from video')
    clip_parser.add_argument("input", help="Input video file")
    clip_parser.add_argument("-o", "--output", required=True,
                            help="Output file path")
    clip_parser.add_argument("-s", "--start", required=True,
                            help="Start time (HH:MM:SS or seconds)")
    clip_parser.add_argument("-d", "--duration",
                            help="Duration in seconds")
    clip_parser.add_argument("-e", "--end",
                            help="End time (HH:MM:SS or seconds)")

    args = parser.parse_args()

    if args.command == 'convert':
        success = convert_video(
            args.input, args.output, args.format, args.resolution,
            args.vcodec, args.acodec, args.vbitrate, args.abitrate
        )
    elif args.command == 'clip':
        if args.duration is None and args.end is None:
            print("Error: Either --duration or --end must be specified", file=sys.stderr)
            sys.exit(1)
        success = extract_clip(args.input, args.output, args.start, args.duration, args.end)
    else:
        parser.print_help()
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
