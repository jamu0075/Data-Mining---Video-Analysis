from darkflow.net.build import TFNet
from multiprocessing import Process, Pipe
import cv2
import os.path
import sys
import time


GET_FPS_EVERY = 180  # frames
PREDICTOR_WAIT_TIMEOUT = 1  # s


def project_file(path):
    return os.path.join(
        os.path.dirname(sys.modules['__main__'].__file__), path
    )


def get_bbox(prediction):
    tl, br = prediction['topleft'], prediction['bottomright']
    return (tl['x'], tl['y'], br['x'] - tl['x'], br['y'] - tl['y'])


class Tracker:

    def __init__(self, frame, prediction):
        self.label = prediction['label']
        self.tracker = cv2.TrackerKCF_create()
        self.bbox = get_bbox(prediction)
        self.ok = self.tracker.init(frame, self.bbox)

    def update(self, frame):
        if self.ok:
            self.ok, bbox = self.tracker.update(frame)
            self.bbox = bbox if self.ok else None
        return self.bbox


def predict_loop(conn):
    tfnet = TFNet(options)
    try:
        conn.send([])  # send an empty list to get first image
        while conn.poll(timeout=PREDICTOR_WAIT_TIMEOUT):
            # print("Waiting for image")
            img = conn.recv()
            # print("Recieved image, predicting...")
            pred = tfnet.return_predict(img)
            # print("Done predicting.")
            conn.send(pred)
    except EOFError:
        print("Closed parent connection.")
        pass


options = {
    "pbLoad": project_file("graph/yolo.pb"),
    "metaLoad": project_file("graph/yolo.meta"),
    "threshold": 0.2
}

pred_conn, conn = Pipe()
predictor = Process(target=predict_loop, args=(pred_conn,))
predictor.start()

cam = cv2.VideoCapture(0)
cam_read = True

img_cache = []
trackers = []

print("Press q to quit.")

fct, boxct = 0, 0
start_time = 0
while(cam_read):
    if fct % GET_FPS_EVERY == 0:
        if start_time:
            time_taken = time.time() - start_time
            fps = GET_FPS_EVERY / time_taken
            boxps = boxct / time_taken
            print("cam: {:5.2f} fps, boxes: {:5.2f} fps".format(fps, boxps))
        start_time = time.time()
        box_ct = 0
    fct += 1

    # Capture frame-by-frame
    cam_read, frame = cam.read()

    # to test slowdown, uncomment this and comment the predictor
    # time.sleep(0.1)

    if conn.poll():
        predictions = conn.recv()
        trackers = [Tracker(img_cache[0], p) for p in predictions]

        for img in img_cache:
            for t in trackers:
                t.update(img)

        conn.send(frame)
        img_cache = [frame]
        boxct += 1

    for i, tkr in enumerate(trackers):
        bbox = tkr.update(frame) if fct % len(trackers) == i else tkr.bbox
        if bbox is not None:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 0, 255), thickness=3)
            cv2.putText(
                frame, tkr.label, p1,
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 255), thickness=2
            )

    # Display the resulting frame
    cv2.imshow('hello', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()
conn.close()
print("Predictor connection closed.")

predictor.join()
