import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time


def decode(im):
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)

    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data, '\n')

    if len(decodedObjects) > 0:
        print(decodedObjects)

    return decodedObjects


# Display barcode and QR code location
def display(im, decodedObjects):
    # Loop over all decoded objects
    iter = 0
    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0, n):
            cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        cv2.putText(im, str(decodedObject.data) + ' (' + decodedObject.type + ')',
                    (20, 40 + iter * 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        iter += 1

    # Display results
    # cv2.imshow("Results", im)
    # cv2.waitKey(0)
    return im


def check_video():
    url = 'http://192.168.55.188:4747/video'
    cap = cv2.VideoCapture(url)

    is_writing_video = False
    video_writer = None
    video_filename = 'barcode.avi'
    video_encoding = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    start_time = None
    fps_estimate = None
    frames_elapsed = int(0)

    while True:
        # capture frame-by-frame
        ret, frame = cap.read()
        # print(type(frame))

        decodedObjects = decode(frame)

        updated_frame = display(frame, decodedObjects)
        # print(type(updated_frame))

        # Update the FPS estimate and related variables.
        if frames_elapsed == 0:
            start_time = time.time()
        else:
            time_elapsed = time.time() - start_time
            fps_estimate = frames_elapsed / time_elapsed

        frames_elapsed += 1

        cv2.imshow('frame', updated_frame)

        if is_writing_video:
            if video_writer is None:
                fps = cap.get(cv2.CAP_PROP_FPS)
                if fps <= 0.0:
                    # The capture's FPS is unknown so use an estimate.
                    if frames_elapsed < 20:
                        # Wait until more frames elapse so that the
                        # estimate is more stable.
                        return
                    else:
                        fps = fps_estimate
                size = (int(cap.get(
                    cv2.CAP_PROP_FRAME_WIDTH)),
                        int(cap.get(
                            cv2.CAP_PROP_FRAME_HEIGHT)))
                video_writer = cv2.VideoWriter(
                    video_filename, video_encoding,
                    fps, size)

            video_writer.write(updated_frame)

        keycode = cv2.waitKey(1)
        if keycode == 9:  # tab
            if not is_writing_video:
                is_writing_video = True
            else:
                is_writing_video = False
                video_writer = None
        elif keycode == 27:  # escape
            break

    # when everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def check_image():
    # Read image
    im = cv2.imread('barcode1.jpg')
    print(type(im))

    decodedObjects = decode(im)
    im_results = display(im, decodedObjects)
    print(type(im_results))

    cv2.imshow("Results", im_results)
    cv2.waitKey(0)


# Main
if __name__ == '__main__':
    check_video()
