import pygame
import time
import sys
import os

class Colors:
    """ANSI color codes for terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class KaraokePlayer:
    def __init__(self, audio_file, lyrics_file, song_title="Unknown Song", artist="Unknown Artist"):
        """Initialize the karaoke player with audio and lyrics"""
        self.audio_file = audio_file
        self.lyrics_file = lyrics_file
        self.song_title = song_title
        self.artist = artist
        self.lyrics = []
        self.start_time = None
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()
        
    def load_lyrics(self):
        """Load and parse the LRC lyrics file"""
        print(f"{Colors.CYAN}Loading lyrics from: {os.path.basename(self.lyrics_file)}{Colors.END}")
        
        try:
            with open(self.lyrics_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"{Colors.RED}✗ Lyrics file not found!{Colors.END}")
            return False
        
        for line in lines:
            line = line.strip()
            if not line or ']' not in line:
                continue
            
            # Find the ] bracket
            bracket_pos = line.find(']')
            
            # Extract timestamp and text
            timestamp = line[1:bracket_pos]  # Skip the [
            text = line[bracket_pos + 1:].strip()
            
            # Skip empty text lines
            if not text:
                continue
            
            # Convert timestamp to seconds
            # Format: MM:SS.CS (minutes:seconds.centiseconds)
            try:
                parts = timestamp.split(':')
                minutes = int(parts[0])
                sec_parts = parts[1].split('.')
                seconds = int(sec_parts[0])
                centiseconds = int(sec_parts[1]) if len(sec_parts) > 1 else 0
                
                total_seconds = minutes * 60 + seconds + centiseconds / 100.0
                
                self.lyrics.append({
                    'time': total_seconds,
                    'text': text,
                    'timestamp': timestamp
                })
            except:
                continue
        
        if not self.lyrics:
            print(f"{Colors.RED}✗ No valid lyrics found in file!{Colors.END}")
            return False
        
        # Sort lyrics by time (just in case)
        self.lyrics.sort(key=lambda x: x['time'])
        
        # Calculate total duration
        total_duration = self.lyrics[-1]['time']
        
        print(f"{Colors.GREEN}✓ Loaded {len(self.lyrics)} lines of lyrics!{Colors.END}")
        print(f"{Colors.CYAN}  Duration: {self.format_time(total_duration)}{Colors.END}\n")
        
        return True
        
    def load_audio(self):
        """Load the audio file"""
        print(f"{Colors.CYAN}Loading audio from: {os.path.basename(self.audio_file)}{Colors.END}")
        try:
            pygame.mixer.music.load(self.audio_file)
            print(f"{Colors.GREEN}✓ Audio loaded successfully!{Colors.END}\n")
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ Error loading audio: {e}{Colors.END}")
            return False
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def format_time(self, seconds):
        """Format seconds into MM:SS"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
    
    def get_current_time(self):
        """Get the current playback time"""
        if self.start_time is None:
            return 0
        return time.time() - self.start_time
    
    def play(self):
        """Play the music and display synchronized lyrics"""
        if not self.lyrics:
            print(f"{Colors.RED}No lyrics loaded!{Colors.END}")
            return
        
        print("\n" + Colors.BOLD + Colors.YELLOW + "="*70)
        print(f"         🎤 KARAOKE PLAYER 🎤         ")
        print("="*70 + Colors.END)
        print(f"{Colors.BOLD}{Colors.CYAN}  {self.song_title} - {self.artist}{Colors.END}")
        print(f"\n{Colors.GREEN}🔊 Audio playback enabled!{Colors.END}")
        print(f"{Colors.CYAN}📝 {len(self.lyrics)} lyrics lines ready{Colors.END}")
        print(f"\n{Colors.DIM}Starting in 3 seconds...{Colors.END}")
        time.sleep(3)
        
        # Clear screen and start
        self.clear_screen()
        
        # Start playing the music
        pygame.mixer.music.play()
        self.start_time = time.time()
        
        displayed_lines = []
        current_line_index = 0
        last_update_time = 0
        
        # Main playback loop
        while True:
            # Check if music is still playing
            if not pygame.mixer.music.get_busy():
                break
            
            # Get current playback time
            current_time = self.get_current_time()
            
            # Check if we need to display the next lyric
            should_update = False
            
            if current_line_index < len(self.lyrics):
                next_lyric = self.lyrics[current_line_index]
                
                # Check if it's time to show this lyric
                if current_time >= next_lyric['time']:
                    should_update = True
                    lyric = next_lyric
                    current_line_index += 1
                    displayed_lines.append(lyric['text'])
            
            # Update display if needed or every 0.5 seconds
            if should_update or (current_time - last_update_time) >= 0.5:
                last_update_time = current_time
                
                # Clear screen for update
                self.clear_screen()
                
                # Header
                print("\n" + Colors.BOLD + Colors.HEADER + "="*70)
                print(f"         🎵 NOW PLAYING: {self.song_title} 🎵         ")
                print("="*70 + Colors.END)
                print(f"{Colors.DIM}  by {self.artist}{Colors.END}\n")
                
                # Show previous lines (dimmed) - last 3 lines
                if displayed_lines:
                    num_prev = min(3, len(displayed_lines) - 1) if should_update else min(3, len(displayed_lines))
                    start_idx = max(0, len(displayed_lines) - num_prev - (1 if should_update else 0))
                    
                    for prev_line in displayed_lines[start_idx:len(displayed_lines) - (1 if should_update else 0)]:
                        print(f"{Colors.DIM}  {prev_line}{Colors.END}")
                    
                    if num_prev > 0:
                        print()
                
                # Show current line (highlighted and bold)
                if should_update and displayed_lines:
                    current_lyric_text = displayed_lines[-1]
                    print(Colors.BOLD + Colors.CYAN + "  " + "━" * 66)
                    print(f"  ♪  {Colors.YELLOW}{current_lyric_text}{Colors.CYAN}  ♪")
                    print("  " + "━" * 66 + Colors.END)
                    print()
                elif displayed_lines:
                    print(f"{Colors.BOLD}  {displayed_lines[-1]}{Colors.END}\n")
                
                # Show next line preview (if available)
                if current_line_index < len(self.lyrics):
                    next_line = self.lyrics[current_line_index]
                    time_until_next = next_line['time'] - current_time
                    if time_until_next > 0 and time_until_next < 10:
                        print(f"{Colors.DIM}  Coming up in {time_until_next:.1f}s: {next_line['text']}{Colors.END}\n")
                
                # Progress bar
                total_duration = self.lyrics[-1]['time'] + 10
                progress = min(current_time / total_duration, 1.0)
                bar_width = 50
                filled = int(bar_width * progress)
                bar = "█" * filled + "░" * (bar_width - filled)
                
                print(f"\n  {Colors.GREEN}{bar}{Colors.END}")
                print(f"  {Colors.CYAN}⏱  {self.format_time(current_time)} / ~{self.format_time(total_duration)}{Colors.END}")
                print(f"  {Colors.DIM}Line {len(displayed_lines)}/{len(self.lyrics)}{Colors.END}")
                
                # Volume and controls
                print(f"\n  {Colors.DIM}🔊 Volume: {int(pygame.mixer.music.get_volume() * 100)}%{Colors.END}")
                print(f"  {Colors.DIM}Press Ctrl+C to stop{Colors.END}")
            
            # Small delay to prevent CPU overuse
            time.sleep(0.05)
        
        # Final screen
        time.sleep(1)
        self.clear_screen()
        print("\n" + Colors.BOLD + Colors.GREEN + "="*70)
        print("         🎵 Song Finished! Thanks for singing! 🎵         ")
        print("="*70 + Colors.END + "\n")
        
        # Show statistics
        print(f"{Colors.BOLD}Session Summary:{Colors.END}\n")
        print(f"  Song: {self.song_title}")
        print(f"  Artist: {self.artist}")
        print(f"  Total lines: {len(self.lyrics)}")
        print(f"  Duration: {self.format_time(self.get_current_time())}")
        print()
    
    def stop(self):
        """Stop the music playback"""
        pygame.mixer.music.stop()


def main():
    """Main function to run the karaoke player"""
    
    # ============================================================
    # CONFIGURATION - UPDATE THESE FOR YOUR SONG!
    # ============================================================
    
    # Song information
    SONG_TITLE = "Birds of a Feather"
    ARTIST = "Billie Eilish"
    
    # File paths - Use raw strings (r"...") for Windows paths
    AUDIO_FILE = r"C:\Users\sabin\Desktop\lyrics-bro\Billie Eilish - BIRDS OF A FEATHER (Official Music Video).mp3"
    LYRICS_FILE = r"C:\Users\sabin\Desktop\lyrics-bro\BOF_complete.lrc"
    
    # ============================================================
    # Example configurations for different songs:
    # ============================================================
    
    # Coldplay - Yellow
    # SONG_TITLE = "Yellow"
    # ARTIST = "Coldplay"
    # AUDIO_FILE = r"C:\Users\sabin\Desktop\lyrics-bro\Coldplay - Yellow.mp3"
    # LYRICS_FILE = r"C:\Users\sabin\Desktop\lyrics-bro\yellow_early.lrc"
    
    # Any other song
    # SONG_TITLE = "Your Song Title"
    # ARTIST = "Artist Name"
    # AUDIO_FILE = r"C:\path\to\your\song.mp3"
    # LYRICS_FILE = r"C:\path\to\your\lyrics.lrc"
    
    # ============================================================
    
    print("\n" + Colors.BOLD + Colors.CYAN + "="*70)
    print("         🎤 UNIVERSAL KARAOKE PLAYER 🎤         ")
    print("="*70 + Colors.END + "\n")
    
    # Check if files exist
    if not os.path.exists(AUDIO_FILE):
        print(f"{Colors.RED}Error: Audio file not found!{Colors.END}")
        print(f"{Colors.YELLOW}Looking for: {AUDIO_FILE}{Colors.END}")
        print(f"\n{Colors.CYAN}Steps to fix:{Colors.END}")
        print(f"  1. Make sure the MP3 file exists")
        print(f"  2. Update the AUDIO_FILE path in the code")
        print(f"  3. Use raw strings: r\"C:\\path\\to\\file.mp3\"")
        input("\nPress Enter to exit...")
        return
    
    if not os.path.exists(LYRICS_FILE):
        print(f"{Colors.RED}Error: Lyrics file not found!{Colors.END}")
        print(f"{Colors.YELLOW}Looking for: {LYRICS_FILE}{Colors.END}")
        print(f"\n{Colors.CYAN}How to get lyrics:{Colors.END}")
        print(f"  1. Run: python download_lyrics.py")
        print(f"  2. Enter artist and song name")
        print(f"  3. Or download from lrclib.net manually")
        print(f"  4. Update the LYRICS_FILE path in the code")
        input("\nPress Enter to exit...")
        return
    
    # Create the karaoke player
    player = KaraokePlayer(AUDIO_FILE, LYRICS_FILE, SONG_TITLE, ARTIST)
    
    # Load files
    if not player.load_lyrics():
        input("\nPress Enter to exit...")
        return
        
    if not player.load_audio():
        input("\nPress Enter to exit...")
        return
    
    # Show instructions
    print(Colors.BOLD + "🎤 Karaoke Mode Ready!" + Colors.END)
    print(f"\n{Colors.GREEN}Features:{Colors.END}")
    print(f"  ✓ Full audio playback")
    print(f"  ✓ Synchronized lyrics")
    print(f"  ✓ Progress tracking")
    print(f"  ✓ Next line preview")
    print(f"\n{Colors.YELLOW}Controls:{Colors.END}")
    print(f"  • Press Enter to start")
    print(f"  • Press Ctrl+C to stop anytime")
    
    input(f"\n{Colors.GREEN}Press Enter to start karaoke...{Colors.END}")
    
    # Start playing!
    player.play()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⏹  Karaoke stopped. Thanks for singing!{Colors.END}\n")
        pygame.mixer.music.stop()
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}\n")
        import traceback
        traceback.print_exc()
        pygame.mixer.music.stop()
        input("\nPress Enter to exit...")
        sys.exit(1)
