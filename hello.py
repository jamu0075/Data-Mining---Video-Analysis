from darkflow.net.build import TFNet
import cv2
import os.path
import sys
import time


GET_FPS_EVERY = 60  # frames


def project_file(path):
    return os.path.join(
        os.path.dirname(sys.modules['__main__'].__file__), path
    )


def coordToTuple(coord):
    return (coord['x'], coord['y'])


options = {
    "pbLoad": project_file("graph/yolo.pb"),
    "metaLoad": project_file("graph/yolo.meta"),
    "threshold": 0.1
}

tfnet = TFNet(options)

cam = cv2.VideoCapture(0)
camRead = True

print("Press q to quit.")

fct = 0
start_time = 0
while(camRead):
    if fct % GET_FPS_EVERY == 0:
        if start_time:
            time_taken = time.time() - start_time
            fps = GET_FPS_EVERY / time_taken
            print("cam: {:5.2f} fps, boxes: {:5.2f} fps".format(fps, fps))
        start_time = time.time()
    fct += 1

    # Capture frame-by-frame
    camRead, frame = cam.read()

    # to test slowdown, uncomment this and comment the predictor
    # time.sleep(0.1)

    predictions = tfnet.return_predict(frame)
    for p in predictions:
        tl, br = coordToTuple(p['topleft']), coordToTuple(p['bottomright'])
        cv2.rectangle(
            frame, tl, br, (0, 0, 255), thickness=3
        )

    # Display the resulting frame
    cv2.imshow('hello', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()
