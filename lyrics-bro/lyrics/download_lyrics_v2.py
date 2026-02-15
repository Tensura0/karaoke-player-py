import requests
import json
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

def download_synced_lyrics(artist, song, output_file="lyrics.lrc"):
    """
    Download synchronized lyrics from LRClib API
    
    Args:
        artist (str): Artist name
        song (str): Song title
        output_file (str): Output filename (default: lyrics.lrc)
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    print(f"{Colors.CYAN}Searching for lyrics...{Colors.END}")
    print(f"  Artist: {Colors.BOLD}{artist}{Colors.END}")
    print(f"  Song: {Colors.BOLD}{song}{Colors.END}\n")
    
    # LRClib API endpoint
    api_url = "https://lrclib.net/api/search"
    
    # Search parameters
    params = {
        "artist_name": artist,
        "track_name": song
    }
    
    try:
        # Make the API request with retry logic and SSL handling
        print(f"{Colors.DIM}Attempting connection...{Colors.END}")
        
        # Try with SSL verification first
        try:
            response = requests.get(api_url, params=params, timeout=15)
        except requests.exceptions.SSLError:
            # If SSL fails, try without verification (less secure but works)
            print(f"{Colors.YELLOW}⚠ SSL verification failed, trying alternate method...{Colors.END}")
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(api_url, params=params, timeout=15, verify=False)
        
        if response.status_code == 200:
            results = response.json()
            
            if not results:
                print(f"{Colors.RED}✗ No lyrics found for this song{Colors.END}")
                return False
            
            # Get the first result (usually the best match)
            result = results[0]
            
            # Check if synchronized lyrics are available
            if not result.get('syncedLyrics'):
                print(f"{Colors.YELLOW}⚠ Found lyrics but no synchronized timestamps{Colors.END}")
                
                # Check if plain lyrics are available
                if result.get('plainLyrics'):
                    print(f"{Colors.CYAN}Plain lyrics are available (no timing){Colors.END}")
                return False
            
            # Get synchronized lyrics
            synced_lyrics = result['syncedLyrics']
            
            # Display info about what we found
            print(f"{Colors.GREEN}✓ Found synchronized lyrics!{Colors.END}\n")
            print(f"  Track: {result.get('trackName', 'Unknown')}")
            print(f"  Artist: {result.get('artistName', 'Unknown')}")
            print(f"  Album: {result.get('albumName', 'Unknown')}")
            print(f"  Duration: {result.get('duration', 0)} seconds")
            
            # Count lyrics lines
            lines = [l for l in synced_lyrics.split('\n') if l.strip() and '[' in l]
            print(f"  Lines: {len(lines)}\n")
            
            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(synced_lyrics)
            
            print(f"{Colors.GREEN}✓ Lyrics saved to: {output_file}{Colors.END}\n")
            
            # Show preview
            print(f"{Colors.BOLD}Preview (first 5 lines):{Colors.END}")
            preview_lines = synced_lyrics.split('\n')[:5]
            for line in preview_lines:
                if line.strip():
                    print(f"  {line}")
            print()
            
            return True
            
        else:
            print(f"{Colors.RED}✗ API request failed (Status: {response.status_code}){Colors.END}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}✗ Connection timeout - website is slow or unreachable{Colors.END}")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"{Colors.RED}✗ Connection error - check your internet connection{Colors.END}")
        print(f"{Colors.DIM}Details: {e}{Colors.END}")
        return False
    except requests.exceptions.SSLError as e:
        print(f"{Colors.RED}✗ SSL Error - secure connection failed{Colors.END}")
        print(f"{Colors.YELLOW}This might be due to:{Colors.END}")
        print(f"  - Antivirus/firewall blocking SSL connections")
        print(f"  - Outdated SSL certificates")
        print(f"  - Network security settings")
        print(f"\n{Colors.CYAN}Try running: pip install --upgrade certifi{Colors.END}")
        return False
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")
        return False


def main():
    """Main function"""
    
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.CYAN}  🎵 LYRICS DOWNLOADER - LRClib API 🎵{Colors.END}")
    print("="*70 + "\n")
    
    print(f"{Colors.BOLD}Download synchronized lyrics for your karaoke songs!{Colors.END}\n")
    
    while True:
        print("="*70)
        
        # Get artist name
        print(f"\n{Colors.CYAN}{Colors.BOLD}Step 1: Enter Artist Name{Colors.END}")
        print(f"{Colors.DIM}(or type 'q' to quit){Colors.END}")
        artist = input(f"{Colors.GREEN}Artist: {Colors.END}").strip()
        
        if artist.lower() == 'q':
            print(f"\n{Colors.CYAN}Thanks for using Lyrics Downloader! 🎵{Colors.END}\n")
            break
        
        if not artist:
            print(f"{Colors.RED}Artist name cannot be empty!{Colors.END}")
            continue
        
        # Get song title
        print(f"\n{Colors.CYAN}{Colors.BOLD}Step 2: Enter Song Title{Colors.END}")
        song = input(f"{Colors.GREEN}Song: {Colors.END}").strip()
        
        if not song:
            print(f"{Colors.RED}Song title cannot be empty!{Colors.END}")
            continue
        
        # Suggest output filename
        suggested_filename = f"{artist} - {song}.lrc"
        # Replace invalid characters for filenames
        suggested_filename = suggested_filename.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}Step 3: Output Filename{Colors.END}")
        print(f"{Colors.DIM}Suggested: {suggested_filename}{Colors.END}")
        print(f"{Colors.DIM}(Press Enter to use suggested, or type your own){Colors.END}")
        filename = input(f"{Colors.GREEN}Filename: {Colors.END}").strip()
        
        if not filename:
            filename = suggested_filename
        
        # Make sure it ends with .lrc
        if not filename.lower().endswith('.lrc'):
            filename += '.lrc'
        
        # Download
        print()
        success = download_synced_lyrics(artist, song, filename)
        
        if success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Success!{Colors.END}")
            print(f"{Colors.CYAN}You can now use '{filename}' with your karaoke player!{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Failed to download lyrics{Colors.END}")
            print(f"{Colors.YELLOW}Possible reasons:{Colors.END}")
            print(f"  - Song not found in database")
            print(f"  - Artist or song name spelled incorrectly")
            print(f"  - No synchronized lyrics available for this song")
            print(f"\n{Colors.CYAN}💡 Tips:{Colors.END}")
            print(f"  - Try different spelling (e.g., 'feat.' vs 'featuring')")
            print(f"  - Try without extra text (e.g., 'Yellow' not 'Yellow - Remastered')")
            print(f"  - Check the exact spelling on streaming services")
        
        # Ask if user wants to download another
        print(f"\n{Colors.BOLD}Download another song?{Colors.END}")
        again = input(f"{Colors.YELLOW}(y/n): {Colors.END}").strip().lower()
        
        if again != 'y':
            print(f"\n{Colors.CYAN}Thanks for using Lyrics Downloader! 🎵{Colors.END}\n")
            break
        
        print()  # Empty line for spacing


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Cancelled by user{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}\n")