#!/usr/bin/env python
from os import chdir
from pytube import YouTube
from helpers import path_relative, DIR_RAW_VIDEOS

chdir(path_relative(DIR_RAW_VIDEOS))

clips = {
    "nyc_intersection": "https://youtu.be/MBxv-OnUZhU",
    "nyc_driving_pov": "https://www.youtu.be/7HaJArMDKgI",
    "biking_indonesia": "https://youtu.be/V98uMzYBlxU",
    "port_nassau": "https://youtu.be/CXECg509GJk"
}

for filename, url in clips.items():
    YouTube(url).streams.first().download(filename=filename)
    print("\a", end="", flush=True)

print("\a\a\a", end="", flush=True)
