# YouTube Downloader Scripts

A collection of Python scripts for downloading and processing YouTube videos using yt-dlp and FFmpeg.

## Prerequisites

- Python 3.7 or higher
- FFmpeg installed on your system

### Installing FFmpeg

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html and add to PATH

## Setup

1. Create and activate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Scripts

### 1. download_video.py - Download YouTube Videos

Download YouTube videos in various qualities and formats.

**Usage:**
```bash
python download_video.py <URL> [OPTIONS]

Options:
  -o, --output PATH       Output directory (default: downloads)
  -q, --quality QUALITY   Video quality: best, 1080p, 720p, 480p, 360p (default: best)
  -f, --format FORMAT     Output format: mp4, webm, mkv (default: mp4)
```

**Examples:**
```bash
# Download video in best quality
python download_video.py "https://youtube.com/watch?v=VIDEO_ID"

# Download in 720p as MP4
python download_video.py "https://youtube.com/watch?v=VIDEO_ID" -q 720p -f mp4

# Download to specific directory
python download_video.py "https://youtube.com/watch?v=VIDEO_ID" -o ~/Videos
```

### 2. download_audio.py - Extract Audio from YouTube Videos

Download and extract audio from YouTube videos.

**Usage:**
```bash
python download_audio.py <URL> [OPTIONS]

Options:
  -o, --output PATH     Output directory (default: downloads/audio)
  -f, --format FORMAT   Audio format: mp3, m4a, wav, flac, opus (default: mp3)
  -q, --quality KBPS    Audio quality: 320, 256, 192, 128, 96 (default: 192)
```

**Examples:**
```bash
# Download audio as MP3
python download_audio.py "https://youtube.com/watch?v=VIDEO_ID"

# Download as FLAC at highest quality
python download_audio.py "https://youtube.com/watch?v=VIDEO_ID" -f flac -q 320

# Download to specific directory
python download_audio.py "https://youtube.com/watch?v=VIDEO_ID" -o ~/Music
```

### 3. download_playlist.py - Download YouTube Playlists

Download entire YouTube playlists or channels.

**Usage:**
```bash
python download_playlist.py <URL> [OPTIONS]

Options:
  -o, --output PATH       Output directory (default: downloads/playlists)
  -q, --quality QUALITY   Video quality: best, 1080p, 720p, 480p, 360p (default: best)
  -f, --format FORMAT     Output format: mp4, webm, mkv (default: mp4)
  -a, --audio-only        Download only audio as MP3
  -s, --start NUMBER      Start from video number (default: 1)
  -e, --end NUMBER        Stop at video number
```

**Examples:**
```bash
# Download entire playlist
python download_playlist.py "https://youtube.com/playlist?list=PLAYLIST_ID"

# Download playlist as audio only
python download_playlist.py "https://youtube.com/playlist?list=PLAYLIST_ID" -a

# Download videos 5 through 10 from playlist
python download_playlist.py "https://youtube.com/playlist?list=PLAYLIST_ID" -s 5 -e 10
```

### 4. convert_video.py - Convert and Process Videos

Convert videos to different formats and resolutions using FFmpeg.

**Convert Command:**
```bash
python convert_video.py convert <INPUT_FILE> [OPTIONS]

Options:
  -o, --output PATH         Output file path
  -f, --format FORMAT       Output format: mp4, webm, mkv, avi (default: mp4)
  -r, --resolution RES      Output resolution (e.g., 1920x1080, 1280x720)
  --vcodec CODEC            Video codec (default: libx264)
  --acodec CODEC            Audio codec (default: aac)
  --vbitrate BITRATE        Video bitrate (e.g., 2M)
  --abitrate BITRATE        Audio bitrate (default: 192k)
```

**Clip Command:**
```bash
python convert_video.py clip <INPUT_FILE> -o <OUTPUT_FILE> [OPTIONS]

Options:
  -o, --output PATH         Output file path (required)
  -s, --start TIME          Start time (HH:MM:SS or seconds) (required)
  -d, --duration SECONDS    Duration in seconds
  -e, --end TIME            End time (HH:MM:SS or seconds)
```

**Examples:**
```bash
# Convert video to MP4 with H.265 codec
python convert_video.py convert input.mkv -o output.mp4 --vcodec libx265

# Convert and resize video to 720p
python convert_video.py convert input.mp4 -r 1280x720 -o output_720p.mp4

# Extract clip from 30 seconds to 1 minute
python convert_video.py clip input.mp4 -o clip.mp4 -s 30 -d 30

# Extract clip using timestamps
python convert_video.py clip input.mp4 -o clip.mp4 -s 00:01:30 -e 00:03:45
```

## Directory Structure

```
ytdownload/
├── venv/                      # Virtual environment
├── downloads/                 # Default download directory
│   ├── audio/                # Audio downloads
│   └── playlists/            # Playlist downloads
├── download_video.py         # Video downloader
├── download_audio.py         # Audio downloader
├── download_playlist.py      # Playlist downloader
├── convert_video.py          # Video converter
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Tips

1. Always keep yt-dlp updated for best compatibility:
   ```bash
   pip install --upgrade yt-dlp
   ```

2. Check available formats for a video:
   ```bash
   yt-dlp -F "https://youtube.com/watch?v=VIDEO_ID"
   ```

3. The scripts will create output directories automatically if they don't exist.

## Troubleshooting

**FFmpeg not found:**
- Make sure FFmpeg is installed and available in your PATH
- Test by running: `ffmpeg -version`

**Download errors:**
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Some videos may be geo-restricted or require authentication

**Permission errors:**
- Make sure you have write permissions in the output directory
- Try using a different output directory with `-o` flag

## License

These scripts are provided as-is for educational and personal use.
