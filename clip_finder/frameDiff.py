#!/usr/bin/python
import cv2
import matplotlib.pyplot as plt
import numpy as np


vidcap = cv2.VideoCapture('/home/user/DM_Videos/Indonesia_Raw.mp4') #30 fps
# fps = vidcap.get(cv2.cv.CV_CAP_PROP_FPS)
# print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
success,current_frame = vidcap.read()
previous_frame = current_frame

frame_diffs = []
results = open("results-test.txt", "w+")

#while(vidcap.isOpened()):
for i in range(3600):
    if i >= 1800:
        current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

        frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
        results.write("%d\r\n" % (sum(sum(frame_diff))))
        frame_diffs.append(sum(sum(frame_diff)))
        #cv2.imshow('frame diff ',frame_diff)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        # if i%1000 == 0:
        #     print(i)
        previous_frame = current_frame.copy()
        ret, current_frame = vidcap.read()

results.close()
#print(np.mean(frame_diffs))
#plt.plot(frame_diffs)
#plt.show()

vidcap.release()
cv2.destroyAllWindows()
