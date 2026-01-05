#!/usr/bin/env python3
"""
YouTube Audio Downloader
Downloads audio from YouTube videos in various formats
"""

import yt_dlp
import argparse
import sys
from pathlib import Path


def download_audio(url, output_path="downloads/audio", audio_format="mp3", quality="192",
                   no_check_certificate=False):
    """
    Download audio from a YouTube video

    Args:
        url: YouTube video URL
        output_path: Directory to save the audio
        audio_format: Output format (mp3, m4a, wav, flac, opus)
        quality: Audio quality in kbps (320, 256, 192, 128, 96)
        no_check_certificate: Skip SSL certificate verification (use for SSL errors)
    """
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': quality,
        }],
        'progress_hooks': [progress_hook],
        'nocheckcertificate': True,  # Skip SSL certificate verification
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from: {url}")
            info = ydl.extract_info(url, download=True)
            print(f"\nSuccessfully extracted audio: {info.get('title', 'audio')}")
            return True
    except Exception as e:
        print(f"Error downloading audio: {e}", file=sys.stderr)
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
        print("\nDownload complete, extracting audio...")


def main():
    parser = argparse.ArgumentParser(description="Download audio from YouTube videos")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", default="downloads/audio",
                       help="Output directory (default: downloads/audio)")
    parser.add_argument("-f", "--format", default="mp3",
                       choices=["mp3", "m4a", "wav", "flac", "opus"],
                       help="Audio format (default: mp3)")
    parser.add_argument("-q", "--quality", default="192",
                       choices=["320", "256", "192", "128", "96"],
                       help="Audio quality in kbps (default: 192)")
    parser.add_argument("--no-check-certificate", action="store_true",
                       help="Skip SSL certificate verification (use if you get SSL errors)")

    args = parser.parse_args()

    success = download_audio(args.url, args.output, args.format, args.quality,
                            args.no_check_certificate)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
