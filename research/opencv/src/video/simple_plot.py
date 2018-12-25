import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as anima


def grab_frame(cap):
    ret, frame = cap.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def close(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)


cap = cv2.VideoCapture(0)

cid = plt.gcf().canvas.mpl_connect('key_press_event', close)

ax = plt.subplot(1, 2, 1)
im = ax.imshow(grab_frame(cap))


def update(i):
    im.set_data(grab_frame(cap))


ani = anima.FuncAnimation(plt.gcf(), update, interval=1)
plt.show()

# when everything done, release the capture
cap.release()
