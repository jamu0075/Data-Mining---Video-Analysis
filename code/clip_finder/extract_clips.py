#!/usr/bin/env python3
import os.path
import cv2
from helpers import path_relative, DIR_RAW_VIDEOS, DIR_CLIPS

N_FRAMES = 500

# taken from data_processing/Video_Breakdown.ipynb
clips = (
    # (source, center, dest)
    ('biking_indonesia.mp4', 539851, 'biking.mp4'),
    ('nyc_intersection.mp4', 47652, 'intersection.mp4'),
    ('port_nassau.mp4', 47193, 'port.mp4')
)

for fname, center, dest in clips:
    infile = path_relative(os.path.join(DIR_RAW_VIDEOS, fname))
    outfile = path_relative(os.path.join(DIR_CLIPS, dest))

    cap = cv2.VideoCapture(infile)
    cap.set(cv2.CAP_PROP_POS_FRAMES, center - N_FRAMES // 2)

    _, frame = cap.read()
    fshape = frame.shape
    fheight, fwidth = fshape[0], fshape[1]
    fourcc = cv2.VideoWriter_fourcc(*'!???')
    out = cv2.VideoWriter(outfile, fourcc, 20.0, (fwidth, fheight))

    for _ in range(N_FRAMES):
        out.write(frame)
        _, frame = cap.read()
