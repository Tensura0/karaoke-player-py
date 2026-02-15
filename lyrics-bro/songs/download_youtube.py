import yt_dlp
import os

class Colors:
    """ANSI color codes"""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def download_youtube_audio(url, output_folder="songs", filename=None):
    """
    Download audio from YouTube video
    
    Args:
        url: YouTube video URL
        output_folder: Folder to save the MP3 (default: songs)
        filename: Custom filename (optional, will use video title if not provided)
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    print(f"\n{Colors.CYAN}Preparing to download...{Colors.END}\n")
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"{Colors.GREEN}✓ Created folder: {output_folder}{Colors.END}\n")
    
    # Configure download options
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best audio quality
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # 192 kbps quality
        }],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Output template
        'quiet': False,  # Show progress
        'no_warnings': False,
    }
    
    # If custom filename provided, use it
    if filename:
        # Remove .mp3 if user added it
        if filename.endswith('.mp3'):
            filename = filename[:-4]
        ydl_opts['outtmpl'] = os.path.join(output_folder, f'{filename}.%(ext)s')
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            print(f"{Colors.CYAN}Fetching video information...{Colors.END}\n")
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            uploader = info.get('uploader', 'Unknown')
            
            # Display video info
            print(f"{Colors.BOLD}Video Information:{Colors.END}")
            print(f"  Title: {title}")
            print(f"  Uploader: {uploader}")
            print(f"  Duration: {duration // 60}:{duration % 60:02d}")
            print()
            
            # Confirm download
            print(f"{Colors.YELLOW}Download this audio?{Colors.END}")
            confirm = input(f"{Colors.GREEN}(y/n): {Colors.END}").strip().lower()
            
            if confirm != 'y':
                print(f"\n{Colors.YELLOW}Download cancelled{Colors.END}\n")
                return False
            
            # Download
            print(f"\n{Colors.CYAN}Downloading and converting to MP3...{Colors.END}\n")
            ydl.download([url])
            
            # Determine final filename
            if filename:
                final_file = os.path.join(output_folder, f"{filename}.mp3")
            else:
                final_file = os.path.join(output_folder, f"{title}.mp3")
            
            print(f"\n{Colors.GREEN}✓ Successfully downloaded!{Colors.END}")
            print(f"{Colors.CYAN}Saved to: {final_file}{Colors.END}\n")
            
            return True
            
    except Exception as e:
        print(f"\n{Colors.RED}✗ Error: {e}{Colors.END}\n")
        return False

def main():
    """Main function with interactive interface"""
    
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.CYAN}  🎵 YOUTUBE AUDIO DOWNLOADER 🎵{Colors.END}")
    print("="*70 + "\n")
    
    print(f"{Colors.BOLD}Download MP3 audio from YouTube videos!{Colors.END}\n")
    
    # Check if yt-dlp is installed
    try:
        import yt_dlp
    except ImportError:
        print(f"{Colors.RED}✗ yt-dlp is not installed!{Colors.END}\n")
        print(f"{Colors.CYAN}To install, run:{Colors.END}")
        print(f"  {Colors.BOLD}pip install yt-dlp{Colors.END}\n")
        return
    
    while True:
        print("="*70)
        
        # Get YouTube URL
        print(f"\n{Colors.CYAN}{Colors.BOLD}Step 1: YouTube URL{Colors.END}")
        print(f"{Colors.DIM}(or type 'q' to quit){Colors.END}")
        url = input(f"{Colors.GREEN}URL: {Colors.END}").strip()
        
        if url.lower() == 'q':
            print(f"\n{Colors.CYAN}Thanks for using YouTube Audio Downloader! 🎵{Colors.END}\n")
            break
        
        if not url:
            print(f"{Colors.RED}URL cannot be empty!{Colors.END}")
            continue
        
        # Validate URL
        if not ('youtube.com' in url or 'youtu.be' in url):
            print(f"{Colors.YELLOW}⚠ Warning: This doesn't look like a YouTube URL{Colors.END}")
            confirm = input(f"{Colors.YELLOW}Continue anyway? (y/n): {Colors.END}").lower()
            if confirm != 'y':
                continue
        
        # Get output folder
        print(f"\n{Colors.CYAN}{Colors.BOLD}Step 2: Output Folder{Colors.END}")
        print(f"{Colors.DIM}Default: songs{Colors.END}")
        print(f"{Colors.DIM}(Press Enter for default){Colors.END}")
        folder = input(f"{Colors.GREEN}Folder: {Colors.END}").strip()
        
        if not folder:
            folder = "songs"
        
        # Get custom filename
        print(f"\n{Colors.CYAN}{Colors.BOLD}Step 3: Custom Filename (Optional){Colors.END}")
        print(f"{Colors.DIM}Leave empty to use video title{Colors.END}")
        print(f"{Colors.DIM}Example: Coldplay - Yellow{Colors.END}")
        filename = input(f"{Colors.GREEN}Filename: {Colors.END}").strip()
        
        if not filename:
            filename = None
        
        # Download
        success = download_youtube_audio(url, folder, filename)
        
        if success:
            print(f"{Colors.GREEN}{Colors.BOLD}✓ Download complete!{Colors.END}")
            print(f"{Colors.CYAN}You can now use this file with your karaoke player!{Colors.END}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}✗ Download failed{Colors.END}")
        
        # Ask if user wants to download another
        print(f"\n{Colors.BOLD}Download another video?{Colors.END}")
        again = input(f"{Colors.YELLOW}(y/n): {Colors.END}").strip().lower()
        
        if again != 'y':
            print(f"\n{Colors.CYAN}Thanks for using YouTube Audio Downloader! 🎵{Colors.END}\n")
            break
        
        print()  # Empty line for spacing

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Cancelled by user{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}\n")
