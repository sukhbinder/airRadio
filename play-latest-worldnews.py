import os
import glob
import subprocess

def latest_matching_mp3(keyword="world", folder="."):
    # find all mp3 files
    files = glob.glob(os.path.join(folder, "*.mp3"))

    # filter by keyword (case insensitive)
    matches = [f for f in files if keyword.lower() in os.path.basename(f).lower()]

    if not matches:
        return None  # or raise exception if you prefer

    # sort by modification time (newest first)
    matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    return matches[0]  # newest match

world = latest_matching_mp3(folder="/tmp/mp3s")
iret = subprocess.run(["nitnem", "-a", world])
