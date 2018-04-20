#!/usr/bin/python
from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=CXECg509GJk').streams.first().download()
