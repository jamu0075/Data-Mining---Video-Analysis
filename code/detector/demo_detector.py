#!/usr/bin/env python
import cv2
import time
from argparse import ArgumentParser
from detector import Detector

GET_FPS_EVERY = 180  # frames


parser = ArgumentParser(description="Detects objects in video.")
parser.add_argument("mp4file", help="The file to detect in. "
                                    "Use 'camera' to detect from camera.")
args = parser.parse_args()


det = Detector()
cap = cv2.VideoCapture(0 if args.mp4file == 'camera' else args.mp4file)
cap_read = True

det.start()

print("Press q to quit.")

prev_det_ct, start_time = 0, 0
while(cap_read):
    if det.frame_count() % GET_FPS_EVERY == 0:

        time_taken = time.time() - start_time
        fps = GET_FPS_EVERY / time_taken

        det_ct = det.detection_count()
        boxps = (det_ct - prev_det_ct) / time_taken
        prev_det_ct = det_ct

        print("cam: {:5.2f} fps, boxes: {:5.2f} fps".format(fps, boxps))

        start_time = time.time()

    # Capture frame-by-frame
    cap_read, frame = cap.read()
    if not cap_read:
        break

    # to test slowdown, uncomment this and comment the predictor
    # time.sleep(0.1)

    for label, bbox in det.update(frame):
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0, 0, 255), thickness=3)
        cv2.putText(
            frame, label, p1,
            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (0, 0, 255), thickness=2
        )

    # Display the resulting frame
    cv2.imshow('hello', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

det.stop()
