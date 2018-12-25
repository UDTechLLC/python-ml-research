import cv2
import numpy

cap = cv2.VideoCapture(0)

# error handling
print(cap.get(3))
print(cap.get(4))

# ret = cap.set(3, 960)
# ret = cap.set(4, 540)

while True:
    # capture frame-by-frame
    ret, frame = cap.read()

    # our operations on the frame come here
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = numpy.fliplr(frame).copy()

    # display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when everything done, release the capture
cap.release()
cv2.destroyAllWindows()
