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


def coordToTuple(coord):
    return (coord['x'], coord['y'])


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

predConn, conn = Pipe()
predictor = Process(target=predict_loop, args=(predConn,))
predictor.start()

cam = cv2.VideoCapture(0)
predictions = []
camRead = True

print("Press q to quit.")

fct, boxct = 0, 0
start_time = 0
while(camRead):
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
    camRead, frame = cam.read()

    # to test slowdown, uncomment this and comment the predictor
    # time.sleep(0.1)

    if conn.poll():
        conn.send(frame)
        predictions = conn.recv()
        boxct += 1

    for p in predictions:
        tl, br = coordToTuple(p['topleft']), coordToTuple(p['bottomright'])
        cv2.rectangle(
            frame, tl, br, (0, 0, 255), thickness=3
        )
        cv2.putText(
            frame, p['label'], tl,
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
print("Predictor connection closed.")

predictor.join()
