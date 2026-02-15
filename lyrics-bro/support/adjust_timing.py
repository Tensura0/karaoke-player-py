import os
import sys

class Colors:
    """ANSI color codes"""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def parse_timestamp(timestamp):
    """
    Parse LRC timestamp to seconds
    Format: MM:SS.CS or MM:SS
    """
    try:
        parts = timestamp.split(':')
        minutes = int(parts[0])
        
        if '.' in parts[1]:
            sec_parts = parts[1].split('.')
            seconds = int(sec_parts[0])
            centiseconds = int(sec_parts[1])
        else:
            seconds = int(parts[1])
            centiseconds = 0
        
        total_seconds = minutes * 60 + seconds + centiseconds / 100.0
        return total_seconds
    except:
        return None

def format_timestamp(seconds):
    """
    Convert seconds back to LRC timestamp format
    Format: MM:SS.CS
    """
    # Handle negative times (shouldn't happen, but just in case)
    if seconds < 0:
        seconds = 0
    
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    secs = int(remaining_seconds)
    centiseconds = int((remaining_seconds - secs) * 100)
    
    return f"{minutes:02d}:{secs:02d}.{centiseconds:02d}"

def adjust_lrc_timing(input_file, output_file, offset_seconds):
    """
    Adjust all timestamps in an LRC file by a given offset
    
    Args:
        input_file (str): Input LRC file path
        output_file (str): Output LRC file path
        offset_seconds (float): Time offset in seconds (positive = delay, negative = advance)
    """
    
    print(f"\n{Colors.CYAN}Adjusting LRC timing...{Colors.END}")
    print(f"  Input: {Colors.BOLD}{input_file}{Colors.END}")
    print(f"  Output: {Colors.BOLD}{output_file}{Colors.END}")
    print(f"  Offset: {Colors.YELLOW}{offset_seconds:+.2f} seconds{Colors.END}")
    
    if offset_seconds > 0:
        print(f"  {Colors.DIM}(Lyrics will appear {offset_seconds:.2f}s later){Colors.END}")
    else:
        print(f"  {Colors.DIM}(Lyrics will appear {abs(offset_seconds):.2f}s earlier){Colors.END}")
    print()
    
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        adjusted_lines = []
        adjusted_count = 0
        
        for line in lines:
            line = line.rstrip('\n\r')
            
            # Check if line contains a timestamp
            if line and '[' in line and ']' in line:
                bracket_start = line.find('[')
                bracket_end = line.find(']')
                
                if bracket_start >= 0 and bracket_end > bracket_start:
                    # Extract timestamp
                    timestamp = line[bracket_start + 1:bracket_end]
                    text = line[bracket_end + 1:]
                    
                    # Parse timestamp
                    time_seconds = parse_timestamp(timestamp)
                    
                    if time_seconds is not None:
                        # Adjust time
                        new_time = time_seconds + offset_seconds
                        
                        # Format new timestamp
                        new_timestamp = format_timestamp(new_time)
                        
                        # Create new line
                        new_line = f"[{new_timestamp}]{text}"
                        adjusted_lines.append(new_line)
                        adjusted_count += 1
                    else:
                        # Couldn't parse, keep original
                        adjusted_lines.append(line)
                else:
                    # No valid brackets, keep original
                    adjusted_lines.append(line)
            else:
                # No timestamp, keep original
                adjusted_lines.append(line)
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(adjusted_lines))
        
        print(f"{Colors.GREEN}✓ Successfully adjusted {adjusted_count} timestamps!{Colors.END}")
        print(f"{Colors.GREEN}✓ Saved to: {output_file}{Colors.END}\n")
        
        # Show preview
        print(f"{Colors.BOLD}Preview (first 5 lines):{Colors.END}")
        for line in adjusted_lines[:5]:
            if line.strip():
                print(f"  {line}")
        print()
        
        return True
        
    except FileNotFoundError:
        print(f"{Colors.RED}✗ Error: Input file not found!{Colors.END}\n")
        return False
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}\n")
        return False

def interactive_mode():
    """Interactive mode to adjust LRC files"""
    
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.CYAN}  🎵 LRC Timing Adjuster 🎵{Colors.END}")
    print("="*70 + "\n")
    
    print(f"{Colors.BOLD}This tool adjusts timing in LRC files to fix sync issues.{Colors.END}\n")
    
    # Get input file
    print(f"{Colors.CYAN}Step 1: Input File{Colors.END}")
    input_file = input("Enter the path to your LRC file: ").strip('"').strip("'")
    
    if not os.path.exists(input_file):
        print(f"\n{Colors.RED}✗ File not found: {input_file}{Colors.END}\n")
        return
    
    # Get offset
    print(f"\n{Colors.CYAN}Step 2: Time Adjustment{Colors.END}")
    print(f"{Colors.DIM}Examples:{Colors.END}")
    print(f"  {Colors.DIM}+2.0  = Lyrics appear 2 seconds later (if lyrics are too early){Colors.END}")
    print(f"  {Colors.DIM}-1.5  = Lyrics appear 1.5 seconds earlier (if lyrics are too late){Colors.END}")
    print(f"  {Colors.DIM}+0.5  = Lyrics appear 0.5 seconds later{Colors.END}")
    
    while True:
        try:
            offset_input = input("\nEnter time offset in seconds (e.g., +2.0 or -1.5): ")
            offset_seconds = float(offset_input)
            break
        except ValueError:
            print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.END}")
    
    # Get output file
    print(f"\n{Colors.CYAN}Step 3: Output File{Colors.END}")
    
    # Suggest a default output filename
    base_name = os.path.splitext(input_file)[0]
    suggested_output = f"{base_name}_adjusted.lrc"
    
    print(f"{Colors.DIM}Suggested: {suggested_output}{Colors.END}")
    output_file = input(f"Enter output filename (press Enter for default): ").strip('"').strip("'")
    
    if not output_file:
        output_file = suggested_output
    
    # Confirm
    print(f"\n{Colors.BOLD}Summary:{Colors.END}")
    print(f"  Input:  {input_file}")
    print(f"  Output: {output_file}")
    print(f"  Offset: {offset_seconds:+.2f} seconds")
    
    confirm = input(f"\n{Colors.YELLOW}Proceed? (y/n): {Colors.END}").lower()
    
    if confirm == 'y':
        adjust_lrc_timing(input_file, output_file, offset_seconds)
        print(f"{Colors.GREEN}{Colors.BOLD}Done! You can now use the adjusted file.{Colors.END}\n")
    else:
        print(f"\n{Colors.YELLOW}Cancelled.{Colors.END}\n")

def quick_adjust(input_file, offset_seconds, output_file=None):
    """Quick adjust mode for command line usage"""
    
    if not output_file:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_adjusted.lrc"
    
    adjust_lrc_timing(input_file, output_file, offset_seconds)

def main():
    """Main function"""
    
    # Check for command line arguments
    if len(sys.argv) >= 3:
        # Command line mode: python adjust_timing.py input.lrc +2.0 [output.lrc]
        input_file = sys.argv[1]
        offset_seconds = float(sys.argv[2])
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        
        quick_adjust(input_file, offset_seconds, output_file)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Cancelled by user{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}\n")
        import traceback
        traceback.print_exc()
