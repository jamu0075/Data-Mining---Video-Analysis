#!/usr/bin/python
import cv2
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser


parser = ArgumentParser(description="frame-differ: computes and stores frame differences")
parser.add_argument('videofile', metavar='mp4file', help="the video to use")
parser.add_argument('savefile', metavar='savefile', help="where to save data")
args = parser.parse_args()

vidcap = cv2.VideoCapture(args.videofile) #30 fps
# fps = vidcap.get(cv2.cv.CV_CAP_PROP_FPS)
# print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
ok, previous_frame = vidcap.read()
ok, current_frame = vidcap.read() if ok else (False, None)

counter = 0
# frame_diffs = []

with open(args.savefile, "w+") as results:

    while ok:

        if counter % 1800 == 0:
            print(counter)

        counter += 1

        current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

        frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
        results.write("%d\r\n" % (sum(sum(frame_diff))))
        #frame_diffs.append(sum(sum(frame_diff)))
        #cv2.imshow('frame diff ',frame_diff)
        #
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        # if i%1000 == 0:
        #     print(i)
        previous_frame = current_frame
        ok, current_frame = vidcap.read()

# print(np.mean(frame_diffs))
#plt.plot(frame_diffs)
#plt.show()

vidcap.release()
# cv2.destroyAllWindows()

print("Done.")
