import cv2
from imutils.video import VideoStream
import warnings
import datetime
import time

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

sampleMillis = 200
previousMillis = 0

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
client = None

# initialize camera, get reference to capture
vs = VideoStream(src=0).start()
print("[INFO] warming up...")
time.sleep(1)

while True:

    timestamp = datetime.datetime.now()
    
    millis = round(time.time() * 1000)
    # if millis - previousMillis < sampleMillis:
    #     continue

    # grab current frame
    frame = vs.read()

    # camera error, frame not grabbed
    if frame is None:
        break

    # detect faces in image
    # frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        image=gray,
        scaleFactor=1.35,
        minNeighbors=5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
        cv2.line(
            frame,
            (int(x+0.5*w), int(y+0.5*h) - 20),
            (int(x+0.5*w), int(y+0.5*h) + 20),
            (0, 0, 255),
            1
        )
        cv2.line(
            frame,
            (int(x+0.5*w) - 20, int(y+0.5*h)),
            (int(x+0.5*w) + 20, int(y+0.5*h)),
            (0, 0, 255),
            1
        )
        cv2.circle(
            frame,
            (int(x+0.5*w), int(y+0.5*h)),
            12,
            (0, 0, 255),
            1
        )

    text = "{0} faces detected".format(len(faces))

    # draw the text and timestamp on the frame
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, text, (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 2)

    cv2.imshow("Facial Recognition", frame)

    previousMillis = millis
    
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, break from the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
vs.stop()
cv2.destroyAllWindows()