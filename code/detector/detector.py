import cv2
from darkflow.net.build import TFNet
from multiprocessing import Process, Pipe
from helpers import path_module_relative


MAX_PREDICTOR_WAIT_TIME = 20  # s

options = {
    "pbLoad": path_module_relative(__name__, "graph/yolo.pb"),
    "metaLoad": path_module_relative(__name__, "graph/yolo.meta"),
    "threshold": 0.2
}


class Detector:

    def start(self):
        self.__pred_conn, self.conn = Pipe()
        self.predictor = Process(target=predict_loop, args=(self.__pred_conn,))

        self.predictor.start()
        # self.fcache = []
        self.trackers = []
        self.fct = 0
        self.boxct = 0

    def stop(self):
        self.conn.send(None)
        self.conn.close()
        self.predictor.join()

    def update(self, frame):
        self.fct += 1
        self.update_detections(frame)
        if self.trackers:
            self.trackers[self.fct % len(self.trackers)].update(frame)
        return ((tkr.label, tkr.bbox) for tkr in self.trackers if tkr.ok)

    def update_detections(self, frame):
        if self.conn.poll():
            predictions = self.conn.recv()
            self.trackers = [Tracker(self.frame_sent, p) for p in predictions]

            # for img in self.fcache:
            #     for t in self.trackers:
            #         t.update(img)

            # update to latest frame
            for t in self.trackers:
                t.update(frame)

            self.conn.send(frame)
            self.frame_sent = frame
            # self.fcache = [frame]
            self.boxct += 1

        else:
            # self.fcache.append(frame)
            pass

    def frame_count(self):
        return self.fct

    def detection_count(self):
        return self.boxct


class Tracker:

    def __init__(self, frame, prediction):
        self.label = prediction['label']
        self.tracker = cv2.TrackerKCF_create()
        self.bbox = self._get_bbox(prediction)
        self.ok = self.tracker.init(frame, self.bbox)

    def update(self, frame):
        self.ok, bbox = self.tracker.update(frame)
        self.bbox = bbox if self.ok else None
        return self.bbox if self.ok else None

    def _get_bbox(self, prediction):
        tl, br = prediction['topleft'], prediction['bottomright']
        return (tl['x'], tl['y'], br['x'] - tl['x'], br['y'] - tl['y'])


def predict_loop(conn):
    tfnet = TFNet(options)
    try:
        conn.send([])  # send an empty list to get first image
        while conn.poll(MAX_PREDICTOR_WAIT_TIME):
            # print("Waiting for image")
            img = conn.recv()
            if img is None:
                return
            # print("Recieved image, predicting...")
            pred = tfnet.return_predict(img)
            # print("Done predicting.")
            conn.send(pred)
        raise RuntimeError("Predictor: connection timed out.")
    except EOFError:
        print("Predictor: parent connection closed.")
