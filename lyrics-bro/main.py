import pygame
import time
import sys
import os
import glob

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

class SongLibrary:
    """Manages the song library and file discovery"""
    
    def __init__(self, music_folder, lyrics_folder=None):
        """
        Initialize SongLibrary
        
        Args:
            music_folder: Path to folder containing MP3 files
            lyrics_folder: Path to folder containing LRC files (optional, defaults to music_folder)
        """
        self.music_folder = music_folder
        self.lyrics_folder = lyrics_folder if lyrics_folder else music_folder
        self.songs = []
        
    def scan_songs(self):
        """Scan the folders for MP3 files and matching LRC files"""
        print(f"\n{Colors.CYAN}Scanning folders:{Colors.END}")
        print(f"  Music: {Colors.BOLD}{self.music_folder}{Colors.END}")
        print(f"  Lyrics: {Colors.BOLD}{self.lyrics_folder}{Colors.END}\n")
        
        # Find all MP3 files
        mp3_pattern = os.path.join(self.music_folder, "*.mp3")
        mp3_files = glob.glob(mp3_pattern)
        
        if not mp3_files:
            print(f"{Colors.RED}✗ No MP3 files found in folder!{Colors.END}")
            print(f"{Colors.YELLOW}Looking in: {self.music_folder}{Colors.END}")
            return False
        
        print(f"{Colors.GREEN}✓ Found {len(mp3_files)} MP3 file(s){Colors.END}")
        
        # Also show LRC files found
        lrc_pattern = os.path.join(self.lyrics_folder, "*.lrc")
        lrc_files = glob.glob(lrc_pattern)
        print(f"{Colors.CYAN}✓ Found {len(lrc_files)} LRC file(s){Colors.END}\n")
        
        # For each MP3, check if there's a matching LRC file
        for mp3_path in mp3_files:
            mp3_filename = os.path.basename(mp3_path)
            mp3_name = os.path.splitext(mp3_filename)[0]
            
            # Look for matching LRC file in lyrics folder
            # Try exact match first
            lrc_path = os.path.join(self.lyrics_folder, f"{mp3_name}.lrc")
            
            # If exact match doesn't exist, look for any LRC with similar name
            if not os.path.exists(lrc_path):
                # Try variations
                possible_lrc = [
                    os.path.join(self.lyrics_folder, f"{mp3_name}_synced.lrc"),
                    os.path.join(self.lyrics_folder, f"{mp3_name}_early.lrc"),
                    os.path.join(self.lyrics_folder, f"{mp3_name}_adjusted.lrc"),
                    os.path.join(self.lyrics_folder, f"{mp3_name}_complete.lrc"),
                ]
                
                for lrc in possible_lrc:
                    if os.path.exists(lrc):
                        lrc_path = lrc
                        break
            
            # Check if LRC exists
            has_lyrics = os.path.exists(lrc_path)
            
            # Try to extract artist and title from filename
            # Common formats: "Artist - Song.mp3" or "Song.mp3"
            if " - " in mp3_name:
                parts = mp3_name.split(" - ", 1)
                artist = parts[0].strip()
                title = parts[1].strip()
            else:
                artist = "Unknown Artist"
                title = mp3_name
            
            self.songs.append({
                'mp3_path': mp3_path,
                'lrc_path': lrc_path if has_lyrics else None,
                'filename': mp3_filename,
                'artist': artist,
                'title': title,
                'has_lyrics': has_lyrics
            })
        
        # Sort by title
        self.songs.sort(key=lambda x: x['title'].lower())
        
        return True
    
    def display_songs(self):
        """Display the list of available songs"""
        print("\n" + "="*70)
        print(f"{Colors.BOLD}{Colors.CYAN}  🎵 AVAILABLE SONGS 🎵{Colors.END}")
        print("="*70 + "\n")
        
        for idx, song in enumerate(self.songs, 1):
            status = f"{Colors.GREEN}✓ Lyrics{Colors.END}" if song['has_lyrics'] else f"{Colors.RED}✗ No lyrics{Colors.END}"
            
            print(f"{Colors.BOLD}{idx}.{Colors.END} {Colors.YELLOW}{song['title']}{Colors.END}")
            print(f"   {Colors.DIM}by {song['artist']}{Colors.END}")
            print(f"   {status}")
            print()
        
        print("="*70 + "\n")
    
    def get_song_by_index(self, index):
        """Get song by index (1-based)"""
        if 1 <= index <= len(self.songs):
            return self.songs[index - 1]
        return None


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
        if not self.lyrics_file:
            print(f"{Colors.YELLOW}⚠ No lyrics file available{Colors.END}")
            print(f"{Colors.CYAN}💡 You can download lyrics using: python download_lyrics.py{Colors.END}\n")
            return False
        
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
            
            bracket_pos = line.find(']')
            timestamp = line[1:bracket_pos]
            text = line[bracket_pos + 1:].strip()
            
            if not text:
                continue
            
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
        
        self.lyrics.sort(key=lambda x: x['time'])
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
        
        print("\n" + Colors.BOLD + Colors.YELLOW + "="*70)
        print(f"         🎤 KARAOKE PLAYER 🎤         ")
        print("="*70 + Colors.END)
        print(f"{Colors.BOLD}{Colors.CYAN}  {self.song_title} - {self.artist}{Colors.END}")
        print(f"\n{Colors.GREEN}🔊 Audio playback enabled!{Colors.END}")
        
        if self.lyrics:
            print(f"{Colors.CYAN}📝 {len(self.lyrics)} lyrics lines ready{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠ Playing audio only (no lyrics){Colors.END}")
        
        print(f"\n{Colors.DIM}Starting in 3 seconds...{Colors.END}")
        time.sleep(3)
        
        # Clear screen and start
        self.clear_screen()
        
        # Start playing the music
        pygame.mixer.music.play()
        self.start_time = time.time()
        
        if not self.lyrics:
            # Audio only mode
            print("\n" + Colors.BOLD + Colors.HEADER + "="*70)
            print(f"         🎵 NOW PLAYING: {self.song_title} 🎵         ")
            print("="*70 + Colors.END)
            print(f"{Colors.DIM}  by {self.artist}{Colors.END}\n")
            print(f"\n{Colors.YELLOW}Audio only - no lyrics available{Colors.END}")
            print(f"{Colors.CYAN}Press Ctrl+C to stop{Colors.END}\n")
            
            # Just wait for music to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        else:
            # Karaoke mode with lyrics
            displayed_lines = []
            current_line_index = 0
            last_update_time = 0
            
            while True:
                if not pygame.mixer.music.get_busy():
                    break
                
                current_time = self.get_current_time()
                should_update = False
                
                if current_line_index < len(self.lyrics):
                    next_lyric = self.lyrics[current_line_index]
                    
                    if current_time >= next_lyric['time']:
                        should_update = True
                        lyric = next_lyric
                        current_line_index += 1
                        displayed_lines.append(lyric['text'])
                
                if should_update or (current_time - last_update_time) >= 0.5:
                    last_update_time = current_time
                    
                    self.clear_screen()
                    
                    # Header
                    print("\n" + Colors.BOLD + Colors.HEADER + "="*70)
                    print(f"         🎵 NOW PLAYING: {self.song_title} 🎵         ")
                    print("="*70 + Colors.END)
                    print(f"{Colors.DIM}  by {self.artist}{Colors.END}\n")
                    
                    # Show previous lines
                    if displayed_lines:
                        num_prev = min(3, len(displayed_lines) - 1) if should_update else min(3, len(displayed_lines))
                        start_idx = max(0, len(displayed_lines) - num_prev - (1 if should_update else 0))
                        
                        for prev_line in displayed_lines[start_idx:len(displayed_lines) - (1 if should_update else 0)]:
                            print(f"{Colors.DIM}  {prev_line}{Colors.END}")
                        
                        if num_prev > 0:
                            print()
                    
                    # Show current line
                    if should_update and displayed_lines:
                        current_lyric_text = displayed_lines[-1]
                        print(Colors.BOLD + Colors.CYAN + "  " + "━" * 66)
                        print(f"  ♪  {Colors.YELLOW}{current_lyric_text}{Colors.CYAN}  ♪")
                        print("  " + "━" * 66 + Colors.END)
                        print()
                    elif displayed_lines:
                        print(f"{Colors.BOLD}  {displayed_lines[-1]}{Colors.END}\n")
                    
                    # Show next line preview
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
                    
                    print(f"\n  {Colors.DIM}🔊 Volume: {int(pygame.mixer.music.get_volume() * 100)}%{Colors.END}")
                    print(f"  {Colors.DIM}Press Ctrl+C to stop{Colors.END}")
                
                time.sleep(0.05)
        
        # Final screen
        time.sleep(1)
        self.clear_screen()
        print("\n" + Colors.BOLD + Colors.GREEN + "="*70)
        print("         🎵 Song Finished! Thanks for singing! 🎵         ")
        print("="*70 + Colors.END + "\n")
        
        print(f"{Colors.BOLD}Session Summary:{Colors.END}\n")
        print(f"  Song: {self.song_title}")
        print(f"  Artist: {self.artist}")
        if self.lyrics:
            print(f"  Total lines: {len(self.lyrics)}")
        print(f"  Duration: {self.format_time(self.get_current_time())}")
        print()
    
    def stop(self):
        """Stop the music playback"""
        pygame.mixer.music.stop()


def main():
    """Main function with interactive menu"""
    
    # ============================================================
    # CONFIGURATION - Set your folders here!
    # ============================================================
    
    # Folder containing MP3 files
    SONGS_FOLDER = r"C:\Users\sabin\Desktop\lyrics-bro\songs"
    
    # Folder containing LRC files
    LYRICS_FOLDER = r"C:\Users\sabin\Desktop\lyrics-bro\lyrics"
    
    # ============================================================
    # Alternative: If everything is in one folder, use this:
    # ============================================================
    # MUSIC_FOLDER = r"C:\Users\sabin\Desktop\lyrics-bro"
    # Then use: library = SongLibrary(MUSIC_FOLDER)
    # ============================================================
    
    print("\n" + Colors.BOLD + Colors.CYAN + "="*70)
    print("         🎤 INTERACTIVE KARAOKE PLAYER 🎤         ")
    print("="*70 + Colors.END + "\n")
    
    # Check if folders exist
    if not os.path.exists(SONGS_FOLDER):
        print(f"{Colors.RED}Error: Songs folder not found!{Colors.END}")
        print(f"{Colors.YELLOW}Looking for: {SONGS_FOLDER}{Colors.END}")
        print(f"\n{Colors.CYAN}Please update SONGS_FOLDER in the code to your actual folder path{Colors.END}")
        input("\nPress Enter to exit...")
        return
    
    if not os.path.exists(LYRICS_FOLDER):
        print(f"{Colors.RED}Error: Lyrics folder not found!{Colors.END}")
        print(f"{Colors.YELLOW}Looking for: {LYRICS_FOLDER}{Colors.END}")
        print(f"\n{Colors.CYAN}Please update LYRICS_FOLDER in the code to your actual folder path{Colors.END}")
        input("\nPress Enter to exit...")
        return
    
    # Scan for songs
    library = SongLibrary(SONGS_FOLDER, LYRICS_FOLDER)
    
    if not library.scan_songs():
        print(f"\n{Colors.CYAN}Make sure you have MP3 files in: {SONGS_FOLDER}{Colors.END}")
        input("\nPress Enter to exit...")
        return
    
    while True:
        # Display available songs
        library.display_songs()
        
        # Get user choice
        print(f"{Colors.BOLD}Enter song number to play (or 'q' to quit):{Colors.END}")
        choice = input(f"{Colors.GREEN}> {Colors.END}").strip()
        
        if choice.lower() == 'q':
            print(f"\n{Colors.CYAN}Thanks for using Karaoke Player! 🎤{Colors.END}\n")
            break
        
        try:
            song_index = int(choice)
            selected_song = library.get_song_by_index(song_index)
            
            if not selected_song:
                print(f"\n{Colors.RED}Invalid choice! Please enter a number from 1 to {len(library.songs)}{Colors.END}")
                time.sleep(2)
                continue
            
            # Check if song has lyrics
            if not selected_song['has_lyrics']:
                print(f"\n{Colors.YELLOW}⚠ Warning: This song has no lyrics file!{Colors.END}")
                print(f"{Colors.CYAN}Audio will play, but no lyrics will be shown.{Colors.END}")
                print(f"\n{Colors.DIM}To add lyrics:{Colors.END}")
                print(f"{Colors.DIM}  1. Run: python download_lyrics.py{Colors.END}")
                print(f"{Colors.DIM}  2. Save to: lyrics/{os.path.splitext(selected_song['filename'])[0]}.lrc{Colors.END}")
                
                confirm = input(f"\n{Colors.YELLOW}Play anyway? (y/n): {Colors.END}").lower()
                if confirm != 'y':
                    continue
            
            # Create karaoke player
            player = KaraokePlayer(
                selected_song['mp3_path'],
                selected_song['lrc_path'],
                selected_song['title'],
                selected_song['artist']
            )
            
            # Load files
            has_lyrics = player.load_lyrics() if selected_song['has_lyrics'] else False
            
            if not player.load_audio():
                input("\nPress Enter to continue...")
                continue
            
            # Show ready message
            print(Colors.BOLD + "🎤 Ready to play!" + Colors.END)
            input(f"\n{Colors.GREEN}Press Enter to start...{Colors.END}")
            
            # Play!
            player.play()
            
            # Ask if user wants to play another song
            print(f"{Colors.CYAN}Play another song?{Colors.END}")
            again = input(f"{Colors.GREEN}(y/n): {Colors.END}").lower()
            
            if again != 'y':
                print(f"\n{Colors.CYAN}Thanks for singing! 🎤{Colors.END}\n")
                break
            
        except ValueError:
            print(f"\n{Colors.RED}Invalid input! Please enter a number.{Colors.END}")
            time.sleep(2)
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Interrupted by user{Colors.END}")
            break


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