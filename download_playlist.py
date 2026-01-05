#!/usr/bin/env python3
"""
YouTube Playlist Downloader
Downloads entire YouTube playlists or channels
"""

import yt_dlp
import argparse
import sys
from pathlib import Path


def download_playlist(url, output_path="downloads/playlists", quality="best",
                     format_type="mp4", audio_only=False, start=1, end=None,
                     no_check_certificate=False):
    """
    Download a YouTube playlist

    Args:
        url: YouTube playlist URL
        output_path: Directory to save videos
        quality: Video quality (best, 1080p, 720p, 480p, 360p)
        format_type: Output format (mp4, webm, mkv)
        audio_only: Download only audio (True/False)
        start: Start downloading from this video number
        end: Stop downloading at this video number
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
        'outtmpl': f'{output_path}/%(playlist_index)s - %(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'ignoreerrors': True,  # Continue on download errors
        'playlist_start': start,
    }

    if end:
        ydl_opts['playlist_end'] = end

    if no_check_certificate:
        ydl_opts['nocheckcertificate'] = True

    if audio_only:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = quality_map.get(quality, quality_map["best"])
        ydl_opts['merge_output_format'] = format_type
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': format_type,
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading playlist from: {url}")
            info = ydl.extract_info(url, download=True)

            if 'entries' in info:
                print(f"\nSuccessfully downloaded playlist: {info.get('title', 'Unknown')}")
                print(f"Total videos downloaded: {len([e for e in info['entries'] if e])}")
            else:
                print("\nDownload completed")

            return True
    except Exception as e:
        print(f"Error downloading playlist: {e}", file=sys.stderr)
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
    parser = argparse.ArgumentParser(description="Download YouTube playlists")
    parser.add_argument("url", help="YouTube playlist URL")
    parser.add_argument("-o", "--output", default="downloads/playlists",
                       help="Output directory (default: downloads/playlists)")
    parser.add_argument("-q", "--quality", default="best",
                       choices=["best", "1080p", "720p", "480p", "360p"],
                       help="Video quality (default: best)")
    parser.add_argument("-f", "--format", default="mp4",
                       choices=["mp4", "webm", "mkv"],
                       help="Output format (default: mp4)")
    parser.add_argument("-a", "--audio-only", action="store_true",
                       help="Download only audio as MP3")
    parser.add_argument("-s", "--start", type=int, default=1,
                       help="Start downloading from this video number (default: 1)")
    parser.add_argument("-e", "--end", type=int,
                       help="Stop downloading at this video number")
    parser.add_argument("--no-check-certificate", action="store_true",
                       help="Skip SSL certificate verification (use if you get SSL errors)")

    args = parser.parse_args()

    success = download_playlist(
        args.url, args.output, args.quality, args.format,
        args.audio_only, args.start, args.end, args.no_check_certificate
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
