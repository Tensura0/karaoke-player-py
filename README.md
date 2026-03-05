# 🎤 Terminal Karaoke System

A complete Python-based karaoke system that downloads songs from YouTube, fetches synchronized lyrics, and plays them in your terminal with real-time lyric display!

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey.svg)
![GitHub stars](https://img.shields.io/github/stars/Tensura0/karaoke-player-py?style=social)

## ✨ Features

- 🎵 **Download audio from YouTube** - Convert any YouTube video to MP3
- 📝 **Automatic lyrics download** - Fetches synchronized lyrics from LRClib API
- 🎤 **Interactive karaoke player** - Real-time lyrics display synced with music
- ⏱️ **Timing adjustment** - Fix lyrics sync issues with timing adjustment tool
- 📁 **Organized library** - Automatic song and lyrics management
- 🎨 **Beautiful terminal UI** - Colorful interface with progress bars
- 🔄 **Song menu** - Browse and select from your music library
- 🎯 **Multiple format support** - Works with MP3 and LRC files

## 📸 Demo

```
🎵 NOW PLAYING: Yellow by Coldplay 🎵

  Look at the stars
  Look how they shine for you

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ♪  And everything you do  ♪
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Coming up in 2.3s: Yeah, they were all yellow

  ██████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░
  ⏱  01:32 / ~03:45
  Line 15/39
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12.8 or lower(for pygame support)
- FFmpeg (for audio conversion)
- Internet connection (for downloads)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tensura0/karaoke-player-py.git
   cd karaoke-player-py
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**
   
   **Windows:**
   - Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to PATH
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Linux:**
   ```bash
   sudo apt install ffmpeg  # Debian/Ubuntu
   sudo yum install ffmpeg  # CentOS/RHEL
   ```

4. **Create required folders**
   ```bash
   mkdir songs lyrics
   ```

5. **Configure paths** (optional)
   
   Edit `main.py` and update these lines if needed:
   ```python
   SONGS_FOLDER = r"./songs"
   LYRICS_FOLDER = r"./lyrics"
   ```

## 📖 Usage

### 1. Download a Song from YouTube

```bash
python download_youtube.py
```

Enter YouTube URL, folder, and filename when prompted.

### 2. Download Synchronized Lyrics

```bash
python download_lyrics.py
```

Enter artist name and song title when prompted. Move the `.lrc` file to the `lyrics/` folder.

### 3. Play Karaoke!

```bash
python main.py
```

Select a song from the menu and start singing! 🎤

### 4. Adjust Timing (if needed)

If lyrics appear too early or too late:

```bash
python adjust_timing.py
```

## 📁 Project Structure

```
karaoke-player-py/
├── main.py                    # Main karaoke player
├── download_youtube.py        # YouTube audio downloader
├── download_lyrics.py         # Lyrics downloader
├── adjust_timing.py           # Timing adjustment tool
├── check_lyrics.py           # Library checker
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── songs/                    # MP3 files go here
│   ├── Coldplay - Yellow.mp3
│   └── Artist - Song.mp3
│
└── lyrics/                   # LRC files go here
    ├── Coldplay - Yellow.lrc
    └── Artist - Song.lrc
```

## 🎯 Complete Workflow

1. **Download audio:** `python download_youtube.py`
2. **Download lyrics:** `python download_lyrics.py`
3. **Move LRC to lyrics folder**
4. **Play karaoke:** `python main.py`
5. **Adjust timing if needed:** `python adjust_timing.py`

## 🛠️ Configuration

### File Naming Convention

For automatic matching, name your files consistently:

```
✅ Good:
songs/Coldplay - Yellow.mp3
lyrics/Coldplay - Yellow.lrc

✅ Also works:
songs/Coldplay - Yellow.mp3
lyrics/Coldplay - Yellow_synced.lrc

❌ Won't match:
songs/Coldplay - Yellow.mp3
lyrics/yellow.lrc
```

## 🔧 Troubleshooting

### "No module named 'pygame'"
```bash
pip install pygame
```

### "FFmpeg not found"
- Make sure FFmpeg is installed
- Verify it's in your PATH: `ffmpeg -version`
- Restart your terminal after installation

### "Lyrics not syncing"
Use the timing adjustment tool:
```bash
python adjust_timing.py
```
- If lyrics appear too late: use negative offset (e.g., `-2.0`)
- If lyrics appear too early: use positive offset (e.g., `+2.0`)

### "Song shows '✗ No lyrics'"
- Check that the LRC file exists in `lyrics/` folder
- Verify the filename matches the MP3 name
- Run `python check_lyrics.py` to diagnose

## 📦 Dependencies

- **pygame** - Audio playback
- **yt-dlp** - YouTube downloading
- **requests** - HTTP requests for lyrics API
- **urllib3** - HTTP client
- **FFmpeg** - Audio format conversion (external dependency)

Install all Python dependencies:
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ideas for Contributions

- GUI version using Tkinter or PyQt
- Playlist support
- Recording functionality
- Web-based interface
- Multi-language support
- Pitch adjustment
- Voice effects

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Disclaimer

This tool is for **personal use only**. Users are responsible for:
- Respecting copyright laws
- Complying with YouTube's Terms of Service
- Only downloading content they have rights to use
- Not distributing copyrighted material

The developers are not responsible for misuse of this software.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloading
- [LRClib](https://lrclib.net/) - Lyrics database
- [pygame](https://www.pygame.org/) - Audio playback
- [FFmpeg](https://ffmpeg.org/) - Audio conversion

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Tensura0/karaoke-player-py/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Tensura0/karaoke-player-py/discussions)

## 🗺️ Roadmap

- [ ] GUI version with PyQt
- [ ] Web interface with Flask
- [ ] Playlist management
- [ ] Voice recording and playback
- [ ] Score calculation based on pitch
- [ ] Cloud sync for song library
- [ ] Mobile app version

---

**Made with ❤️ and Python by [Tensura0](https://github.com/Tensura0)**

⭐ Star this repo if you found it helpful!

🎤 Happy singing! 🎵
