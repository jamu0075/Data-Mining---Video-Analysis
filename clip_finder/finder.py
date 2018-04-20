#!/usr/bin/python

import cv2
vidcap = cv2.VideoCapture('/home/user/DM_Videos/NYC_Traffic.mp4')

success,current_frame = vidcap.read()
previous_frame = current_frame

while(vidcap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)

    cv2.imshow('frame diff ',frame_diff)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(sum(sum(frame_diff)))
    previous_frame = current_frame.copy()
    ret, current_frame = vidcap.read()

vidcap.release()
cv2.destroyAllWindows()
