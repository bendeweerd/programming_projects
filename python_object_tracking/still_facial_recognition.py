import cv2
import argparse
import sys

# construct argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image_path", required=True, help="path to image")
args = vars(ap.parse_args())

cascPath = "haarcascade_frontalface_default.xml"

try:
    imagePath = args.get("image_path", None)
    faceCascade = cv2.CascadeClassifier(cascPath)
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
except:
    print("[ERROR]: Unable to generate image and cascade. Exiting...")
    sys.exit()

# detect faces in image
faces = faceCascade.detectMultiScale(
    image=gray,
    scaleFactor=1.3,
    minNeighbors=5,
    minSize=(30,30),
    flags=cv2.CASCADE_SCALE_IMAGE
)

print("Found {0} faces!".format(len(faces)))

# draw rectangle around faces
for(x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces found", image)
cv2.waitKey(0)
    
