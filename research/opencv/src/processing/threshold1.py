import cv2


def create_resized_window(wndname, image, screen_res=(720, 1280)):
    cv2.namedWindow(wndname, cv2.WINDOW_NORMAL)

    # define the screen resolution
    scale_height = screen_res[0] / image.shape[0]
    scale_width = screen_res[1] / image.shape[1]
    scale = min(scale_height, scale_width)

    # resize window width and height
    window_height = int(image.shape[0] * scale)
    window_width = int(image.shape[1] * scale)
    cv2.resizeWindow(wndname, window_width, window_height)


if __name__ == "__main__":
    # read image in gray scale
    image = cv2.imread('../../../images/napteka1.jpg', cv2.IMREAD_GRAYSCALE)
    create_resized_window('image', image)
    cv2.imshow('image', image)

    ret, thresh1 = cv2.threshold(image, thresh=63, maxval=255, type=cv2.THRESH_BINARY)
    create_resized_window('thresh1', thresh1)
    cv2.imshow('thresh1', thresh1)

    ret, thresh2 = cv2.threshold(image, thresh=63, maxval=191, type=cv2.THRESH_BINARY)
    create_resized_window('thresh2', thresh2)
    cv2.imshow('thresh2', thresh2)

    ret, thresh3 = cv2.threshold(image, thresh=63, maxval=127, type=cv2.THRESH_BINARY)
    create_resized_window('thresh3', thresh3)
    cv2.imshow('thresh3', thresh3)

    thresh4 = cv2.adaptiveThreshold(image, maxValue=255,
                                    adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                    thresholdType=cv2.THRESH_BINARY, blockSize=11, C=2)
    create_resized_window('thresh4', thresh4)
    cv2.imshow('thresh4', thresh4)

    thresh5 = cv2.adaptiveThreshold(image, maxValue=255,
                                    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    thresholdType=cv2.THRESH_BINARY, blockSize=11, C=2)
    create_resized_window('thresh5', thresh5)
    cv2.imshow('thresh5', thresh5)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
