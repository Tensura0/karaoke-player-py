# Contributing to karoake-player-py

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (OS, Python version)
- Error messages or screenshots

### Suggesting Features

Feature requests are welcome! Please open an issue with:
- Clear description of the feature
- Why it would be useful
- How it might work
- Any examples or mockups

### Pull Requests

1. **Fork the repository**
2. **Create a branch** for your feature:
```bash
   git checkout -b feature/AmazingFeature
```
3. **Make your changes**
4. **Test your changes** thoroughly
5. **Commit with clear messages**:
```bash
   git commit -m "Add: Feature description"
```
6. **Push to your fork**:
```bash
   git push origin feature/AmazingFeature
```
7. **Open a Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions
- Keep functions focused and small

### Testing

Before submitting:
- Test on your system
- Make sure all existing features still work
- Test edge cases
- Verify error handling

## Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/karaoke-player-py.git
cd karaoke-player-py

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (see README)

# Run the application
python main.py
```

## Project Structure

- `main.py` - Main karaoke player
- `download_youtube.py` - YouTube downloader
- `download_lyrics.py` - Lyrics fetcher
- `adjust_timing.py` - Timing adjustment tool
- `check_lyrics.py` - Library checker

## Ideas for Contributions

### Easy
- Add more color themes
- Improve error messages
- Add more file format support
- Better progress indicators

### Medium
- Add playlist support
- Implement shuffle/repeat modes
- Add volume controls
- Create configuration file system
- Add search functionality

### Advanced
- Build GUI with Tkinter/PyQt
- Create web interface
- Add voice recording
- Implement pitch detection
- Add score calculation
- Multi-language support

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the code, not the person
- Help others learn and grow

## Questions?

Feel free to open an issue with your question or reach out to the maintainers!

---

**Thank you for contributing! 🎤🎵**
