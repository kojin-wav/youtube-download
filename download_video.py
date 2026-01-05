#!/usr/bin/env python3
"""
YouTube Video Downloader
Downloads YouTube videos in various quality options
"""

import yt_dlp
import argparse
import sys
from pathlib import Path


def download_video(url, output_path="downloads", quality="best", format_type="mp4",
                   no_check_certificate=False):
    """
    Download a YouTube video

    Args:
        url: YouTube video URL
        output_path: Directory to save the video
        quality: Video quality (best, 1080p, 720p, 480p, 360p)
        format_type: Output format (mp4, webm, mkv)
        no_check_certificate: Skip SSL certificate verification (use for SSL errors)
    """
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)

    # Define quality settings
    quality_map = {
        "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
        "720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
        "480p": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]",
        "360p": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]",
    }

    ydl_opts = {
        'format': quality_map.get(quality, quality_map["best"]),
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': format_type,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': format_type,
        }],
        'progress_hooks': [progress_hook],
    }

    if no_check_certificate:
        ydl_opts['nocheckcertificate'] = True

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from: {url}")
            info = ydl.extract_info(url, download=True)
            print(f"\nSuccessfully downloaded: {info.get('title', 'video')}")
            return True
    except Exception as e:
        print(f"Error downloading video: {e}", file=sys.stderr)
        return False


def progress_hook(d):
    """Progress hook to display download progress"""
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded = d.get('downloaded_bytes', 0)
        if total > 0:
            percent = (downloaded / total) * 100
            print(f"\rProgress: {percent:.1f}% ({downloaded}/{total} bytes)", end='')
    elif d['status'] == 'finished':
        print("\nDownload complete, processing...")


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", default="downloads",
                       help="Output directory (default: downloads)")
    parser.add_argument("-q", "--quality", default="best",
                       choices=["best", "1080p", "720p", "480p", "360p"],
                       help="Video quality (default: best)")
    parser.add_argument("-f", "--format", default="mp4",
                       choices=["mp4", "webm", "mkv"],
                       help="Output format (default: mp4)")
    parser.add_argument("--no-check-certificate", action="store_true",
                       help="Skip SSL certificate verification (use if you get SSL errors)")

    args = parser.parse_args()

    success = download_video(args.url, args.output, args.quality, args.format,
                            args.no_check_certificate)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
