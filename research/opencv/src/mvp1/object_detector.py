import cv2


class ObjectDetector(object):
    def __init__(self):
        pass

    def detect(self, image):
        _, contours, h = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cont in contours:
            if cv2.contourArea(cont) > 5000:
                arc_len = cv2.arcLength(cont, True)
                approx = cv2.approxPolyDP(cont, 0.1 * arc_len, True)

                if len(approx) == 4:
                    cv2.drawContours(image, [approx], -1, (0, 0, 255), 2)
                else:
                    pass


class SimpleObjectDetector(ObjectDetector):
    def __init__(self):
        ObjectDetector.__init__(self)

