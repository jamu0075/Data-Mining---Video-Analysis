#!/usr/bin/python
from pytube import YouTube

yt = YouTube('https://youtu.be/V98uMzYBlxU').streams.first().download()
