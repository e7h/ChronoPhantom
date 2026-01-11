import os
import sys
import ctypes
import subprocess
import shutil
import socket
import getpass
from datetime import datetime
from colorama import init, Fore, Style, Back
init(autoreset=True)
FILE_WRITE_ATTRIBUTES = 0x0100
OPEN_EXISTING = 3
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
NEON_CYAN = Fore.CYAN
NEON_PURPLE = Fore.MAGENTA
NEON_PINK = Fore.LIGHTMAGENTA_EX
ELECTRIC_BLUE = Fore.LIGHTCYAN_EX
MATRIX_GREEN = Fore.LIGHTGREEN_EX
GOLD = Fore.LIGHTYELLOW_EX
SILVER = Fore.WHITE
GRAY = Fore.LIGHTBLACK_EX
ERROR_RED = Fore.LIGHTRED_EX

DIM = Style.DIM
BRIGHT = Style.BRIGHT
RST = Style.RESET_ALL
def print_box(text, color=NEON_CYAN, width=60):
    """Print text in a modern box"""
    lines = text.split('\n')
    print(f"{color}┌{'─' * (width - 2)}┐{RST}")
    for line in lines:
        padding = width - len(line) - 4
        print(f"{color}│{RST} {line}{' ' * padding} {color}│{RST}")
    print(f"{color}└{'─' * (width - 2)}┘{RST}")

def print_gradient_line(char="═", width=70):
    """Print a gradient line"""
    colors = [NEON_PURPLE, NEON_PINK, ELECTRIC_BLUE, NEON_CYAN]
    segment_len = width // len(colors)
    line = ""
    for i, color in enumerate(colors):
        line += f"{color}{char * segment_len}"
    print(line + RST)

def die(msg):
    print(f"\n{ERROR_RED}╳ CRITICAL ERROR{RST}")
    print_box(msg, ERROR_RED, 60)
    input(f"\n{GRAY}Press Enter to exit...{RST}")
    sys.exit(1)

def run(cmd):
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def fake_prompt(path="~/ChronoPhantom"):
    return (
        f"{BRIGHT}{NEON_PURPLE}┌─[{RST}"
        f"{NEON_CYAN}{getpass.getuser()}{RST}"
        f"{GRAY}@{RST}"
        f"{ELECTRIC_BLUE}{socket.gethostname()}{RST}"
        f"{BRIGHT}{NEON_PURPLE}]{RST}\n"
        f"{BRIGHT}{NEON_PURPLE}└─▶{RST} "
    )
def parse_date(s):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    die("Invalid date format. Use: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS")

def set_creation_time(path, dt):
    handle = kernel32.CreateFileW(
        path, FILE_WRITE_ATTRIBUTES, 0, None, OPEN_EXISTING, 0, None
    )
    if handle == -1:
        die("Windows API denied file access.")

    ts = int((dt.timestamp() + 11644473600) * 10**7)
    low, high = ts & 0xFFFFFFFF, ts >> 32
    ft = (ctypes.c_ulong * 2)(low, high)

    kernel32.SetFileTime(handle, ft, None, None)
    kernel32.CloseHandle(handle)

def change_fs_dates(path, dt):
    ts = dt.timestamp()
    os.utime(path, (ts, ts))
    set_creation_time(path, dt)
def strip_exif(path):
    run(["exiftool", "-all=", "-overwrite_original", path])

def ffmpeg_rewrite(path):
    tmp = path + ".tmp"
    run(["ffmpeg", "-y", "-i", path, "-map_metadata", "-1", "-c", "copy", tmp])
    if os.path.exists(tmp):
        shutil.move(tmp, path)

def clean_metadata(path):
    ext = os.path.splitext(path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png", ".tiff", ".heic"]:
        strip_exif(path)

    if ext in [".mp4", ".mkv", ".avi", ".mov", ".mp3", ".wav", ".flac"]:
        ffmpeg_rewrite(path)
def process_file(path, dt, clean=False):
    if not os.path.exists(path):
        die(f"File not found: {path}")

    if clean:
        print(f"{GOLD}⟳ Cleaning metadata...{RST}")
        clean_metadata(path)

    change_fs_dates(path, dt)
    print(f"{MATRIX_GREEN}✓ SUCCESS{RST} {GRAY}│{RST} {NEON_CYAN}{path}{RST}")

def process_dir(path, dt, clean=False):
    if not os.path.isdir(path):
        die("Target is not a directory.")

    file_count = 0
    for root, _, files in os.walk(path):
        for f in files:
            process_file(os.path.join(root, f), dt, clean)
            file_count += 1
    
    print(f"\n{MATRIX_GREEN}✓ Processed {file_count} files{RST}")
def banner():
    os.system("cls")
    print_gradient_line("═", 70)
    print(f"""
{BRIGHT}{NEON_PURPLE}    ▄████▄   ██░ ██  ██▀███   ▒█████   ███▄    █  ▒█████  {RST}
{NEON_PINK}   ▒██▀ ▀█  ▓██░ ██▒▓██ ▒ ██▒▒██▒  ██▒ ██ ▀█   █ ▒██▒  ██▒{RST}
{ELECTRIC_BLUE}   ▒▓█    ▄ ▒██▀▀██░▓██ ░▄█ ▒▒██░  ██▒▓██  ▀█ ██▒▒██░  ██▒{RST}
{NEON_CYAN}   ▒▓▓▄ ▄██▒░▓█ ░██ ▒██▀▀█▄  ▒██   ██░▓██▒  ▐▌██▒▒██   ██░{RST}
{NEON_PURPLE}   ▒ ▓███▀ ░░▓█▒░██▓░██▓ ▒██▒░ ████▓▒░▒██░   ▓██░░ ████▓▒░{RST}
{NEON_PINK}   ░ ░▒ ▒  ░ ▒ ░░▒░▒░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░ ▒░▒░▒░ {RST}
{ELECTRIC_BLUE}     ░  ▒    ▒ ░▒░ ░  ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░░   ░ ▒░  ░ ▒ ▒░ {RST}
{NEON_CYAN}   ░         ░  ░░ ░  ░░   ░ ░ ░ ░ ▒     ░   ░ ░ ░ ░ ░ ▒  {RST}
{NEON_PURPLE}   ░ ░       ░  ░  ░   ░         ░ ░           ░     ░ ░  {RST}
{NEON_PINK}   ░         {BRIGHT}PHANTOM{RST}                                   {RST}
""")
    print_gradient_line("═", 70)
    print(f"""
    {NEON_CYAN}[1]{RST} {SILVER}→{RST} Single File Timestamp        {GRAY}│ Modify one file{RST}
    {NEON_CYAN}[2]{RST} {SILVER}→{RST} Batch Directory Processing   {GRAY}│ Recursive operation{RST}
    {NEON_CYAN}[3]{RST} {SILVER}→{RST} {GOLD}★{RST} Deep Clean {GRAY}(Metadata Wipe){RST} {GRAY}│ Maximum stealth{RST}
    {NEON_CYAN}[4]{RST} {SILVER}→{RST} Information                  {GRAY}│ About this tool{RST}
    {NEON_CYAN}[5]{RST} {SILVER}→{RST} Exit                         {GRAY}│ Close application{RST}
""")
    print_gradient_line("─", 70)
def about():
    os.system("cls")
    print_gradient_line("═", 70)
    print(f"""
{BRIGHT}{NEON_PURPLE}╔══════════════════════════════════════════════════════════════════╗{RST}
{BRIGHT}{NEON_PURPLE}║{RST}                      {BRIGHT}{GOLD}CHRONOPHANTOM v2.0{RST}                          {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}╠══════════════════════════════════════════════════════════════════╣{RST}
{BRIGHT}{NEON_PURPLE}║{RST}                                                                  {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}  {NEON_CYAN} Core Features:{RST}                                              {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}     {MATRIX_GREEN}✓{RST} NTFS timestamp manipulation                             {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}     {MATRIX_GREEN}✓{RST} Creation, modification & access time rewrite           {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}     {MATRIX_GREEN}✓{RST} EXIF metadata removal (images)                         {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}     {MATRIX_GREEN}✓{RST} Media container rewrite (video/audio)                  {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}     {MATRIX_GREEN}✓{RST} Recursive directory processing                         {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}                                                                  {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}  {GOLD}⚠ Requirements:{RST}                                               {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}     • Windows OS (NTFS filesystem)                               {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}     • ExifTool (for image metadata)                              {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}     • FFmpeg (for media files)                                   {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}                                                                  {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}  {ELECTRIC_BLUE} Philosophy:{RST}                                               {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}     {GRAY}"If time is evidence, we erase the clock."{RST}                {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}║{RST}              {GOLD}BY : Slay {RST}                                                             {BRIGHT}{NEON_PURPLE}║{RST}
{BRIGHT}{NEON_PURPLE}╚══════════════════════════════════════════════════════════════════╝{RST}
""")
    print_gradient_line("═", 70)
    input(f"\n{GRAY}Press Enter to return to main menu...{RST}")

def success_animation():
    """Display success animation"""
    print(f"\n{MATRIX_GREEN}{'▓' * 50}{RST}")
    print(f"{MATRIX_GREEN}█ OPERATION COMPLETE                                █{RST}")
    print(f"{MATRIX_GREEN}{'▓' * 50}{RST}\n")
def main():
    if os.name != "nt":
        die("This tool requires Windows OS (NTFS filesystem support).")

    while True:
        banner()
        choice = input(fake_prompt()).strip()

        if choice == "5" or choice.lower() in ["exit", "quit", "q"]:
            print(f"\n{GRAY}┌────────────────────────────────┐{RST}")
            print(f"{GRAY}│{RST} {NEON_CYAN}Session terminated.{RST}            {GRAY}│{RST}")
            print(f"{GRAY}│{RST} {DIM}Timeline integrity restored.{RST}  {GRAY}│{RST}")
            print(f"{GRAY}└────────────────────────────────┘{RST}\n")
            break

        if choice == "4":
            about()
            continue

        if choice not in ["1", "2", "3"]:
            print(f"\n{ERROR_RED}✗ Invalid option{RST}")
            input(f"{GRAY}Press Enter to continue...{RST}")
            continue

        print(f"\n{NEON_CYAN}┌─[ INPUT REQUIRED ]{RST}")
        path = input(f"{NEON_CYAN}│{RST} Target path {GRAY}→{RST} ").strip().strip('"')
        date_input = input(f"{NEON_CYAN}│{RST} Target date {GRAY}→{RST} ").strip()
        print(f"{NEON_CYAN}└{'─' * 40}{RST}\n")
        
        dt = parse_date(date_input)

        print(f"{GOLD}⟳ Processing...{RST}\n")

        if choice == "1":
            process_file(path, dt)
        elif choice == "2":
            process_dir(path, dt)
        elif choice == "3":
            if os.path.isfile(path):
                process_file(path, dt, clean=True)
            else:
                process_dir(path, dt, clean=True)

        success_animation()
        input(f"{GRAY}Press Enter to continue...{RST}")

if __name__ == "__main__":
    main()