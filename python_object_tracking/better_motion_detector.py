# import packages
from cv2 import FONT_HERSHEY_SIMPLEX, VideoCapture
from imutils.video import VideoStream
import argparse
import warnings
import datetime
import dropbox
import imutils
import json
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
client = None

# check to see if Dropbox should be used
if conf["use_dropbox"]:
    # not going to use this...
    pass

# initialize camera, get reference to capture
vs = VideoStream(src=0).start()
print("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

while True:
    # grab current frame
    frame = vs.read()
    timestamp = datetime.datetime.now()
    text = "No"

    # camera error, frame not grabbed
    if frame is None:
        break

    # resize frame, convert to grayscale, blur
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if average frame is None, initialize it
    if avg is None:
        print("[INFO] starting background model...")
        avg = gray.copy().astype("float")
        continue

    # accumulate weighted average between current frame
    # and previous frames, compute difference between current
    # frame and running average
    cv2.accumulateWeighted(gray, avg, 0.1)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # threshold the delta image, dilate the thresholded image to fill in holes,
    # then find contours on thresholded image
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over contours
    for c in cnts:
        # if contour is too small, ignore it
        if cv2.contourArea(c) < conf["min_area"]:
            continue
            
        # compute bounding box for contour, draw it on the frame
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Yes"

    # draw the text and timestamp on the frame
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Motion?: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

    	# check to see if the room is occupied
    if text == "Yes":
		# check to see if enough time has passed between uploads
        if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
			# increment the motion counter
            motionCounter += 1
			# check to see if the number of frames with consistent motion is
			# high enough
            if motionCounter >= conf["min_motion_frames"]:
				# check to see if dropbox sohuld be used
                if conf["use_dropbox"]:
					# not going to use this
                    pass
				# update the last uploaded timestamp and reset the motion
				# counter
                lastUploaded = timestamp
                motionCounter = 0
	# otherwise, the room is not occupied
    else:
        motionCounter = 0

    if conf["show_video"]:

        # show the frame and record if user presses a key
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, break from the loop
        if key == ord("q"):
            break

# cleanup the camera and close any open windows
vs.stop()
cv2.destroyAllWindows()