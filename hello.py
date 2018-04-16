from darkflow.net.build import TFNet
from multiprocessing import Process, Pipe
from numpy import array
import cv2
import os.path
import sys
import time


GET_FPS_EVERY = 180  # frames
PREDICTOR_WAIT_TIMEOUT = 1  # s


class Prediction:
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            pred = args[0]
            args = [
                pred['confidence'],
                pred['label'],
                pred['topleft'],
                pred['bottomright']
            ]
        self._setup_from_values(*args)

    def dist_sq(self, prediction):
        return sum((prediction.center - self.center) ** 2)

    def set_velocity_away_from(self, prev):
        self.vtl = self.top_left - prev.top_left
        self.vbr = self.bottom_right - prev.bottom_right

    def get_bounds_after_n_frames(self, nframes):
        tl = self.top_left + self.vtl * nframes
        br = self.bottom_right + self.vbr * nframes
        return tuple(tl), tuple(br)

    def __hash__(self):
        return self.hash

    def _setup_from_values(self, confidence, label, top_left, bottom_right):
        self.confidence = confidence
        self.label = label
        self.top_left = array((top_left['x'], top_left['y']))
        self.bottom_right = array((bottom_right['x'], bottom_right['y']))
        self.center = self.bottom_right - self.top_left
        self.vtl = self.vbr = 0  # in pixels per frame

        # cache hash for fast lookup
        self.hash = hash((
            label, self.top_left[0], self.top_left[1],
            self.bottom_right[0], self.bottom_right[1]
        ))


def project_file(path):
    return os.path.join(
        os.path.dirname(sys.modules['__main__'].__file__), path
    )


def match_objects(objs1, objs2):
    objs1, objs2 = list(map(Prediction, objs1)), list(map(Prediction, objs2))
    matches = {}
    for y in objs2:
        best_dist, best_match = float('inf'), None
        for x in objs1:
            if x in matches or x.label != y.label:
                continue
            dist = x.dist_sq(y)
            if dist < best_dist:
                best_dist, best_match = dist, x
        if best_match:
            matches[best_match] = y
        else:
            print("{} only matched once".format(y.label))
    return matches.items()


def predict_with_velocity(obj_matches):
    for p1, p2 in obj_matches:
        p2.set_velocity_away_from(p1)
        yield p2


def predict_loop(conn):
    tfnet = TFNet(options)
    try:
        conn.send([])  # send an empty list to get first image
        while conn.poll(timeout=PREDICTOR_WAIT_TIMEOUT):
            # print("Waiting for image")
            f1, f2 = conn.recv()
            # print("Recieved image, predicting...")
            pred1, pred2 = (tfnet.return_predict(f) for f in [f1, f2])
            matched_pairs = match_objects(pred1, pred2)
            predictions = list(predict_with_velocity(matched_pairs))
            # print("Done predicting.")
            conn.send(predictions)
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
predictions, sent_fct = [], 0
cam_read, frame = True, None

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
    frame_prev = frame
    cam_read, frame = cam.read()

    # to test slowdown, uncomment this and comment the predictor
    # time.sleep(0.1)

    if conn.poll() and fct > 1:
        conn.send((frame_prev, frame))
        pred_fct = sent_fct
        sent_fct = fct
        predictions = conn.recv()
        boxct += 1

    for p in predictions:
        tl, br = p.get_bounds_after_n_frames(fct - pred_fct)
        cv2.rectangle(frame, tl, br, (0, 0, 255), thickness=3)
        cv2.putText(
            frame, p.label, tl,
            cv2.FONT_HERSHEY_SIMPLEX, 1,
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

print("Closing predictor...", end='', flush=True)
predictor.join()
print("Done.")
