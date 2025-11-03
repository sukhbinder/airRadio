#!/usr/bin/env python3

import os
import glob
import subprocess
import argparse

def latest_matching_mp3(keyword="world", folder="/tmp/mp3s"):
    # find all mp3 files
    files = glob.glob(os.path.join(folder, "*.mp3"))

    # filter by keyword (case insensitive)
    matches = [f for f in files if keyword.lower() in os.path.basename(f).lower()]

    if not matches:
        return None

    # sort by modification time (newest first)
    matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    return matches[0]

def main():
    parser = argparse.ArgumentParser(description="Play latest matching MP3 file")
    
    parser.add_argument(
        "-k", "--keyword",
        default="world",
        help="Keyword to filter MP3 files (default: world)"
    )
    
    parser.add_argument(
        "-f", "--folder",
        default="/tmp/mp3s",
        help="Folder containing MP3 files (default: /tmp/mp3s)"
    )
    
    args = parser.parse_args()

    mp3file = latest_matching_mp3(keyword=args.keyword, folder=args.folder)

    if mp3file:
        print(f"🎧 Playing latest MP3 matching '{args.keyword}': {mp3file}")
        subprocess.run(["nitnem", "-a", mp3file])
    else:
        print(f"⚠️ No MP3 found in '{args.folder}' with keyword '{args.keyword}'")

if __name__ == "__main__":
    main()
