import cv2
import pyzbar.pyzbar as pyzbar


def post_detect(original_image, output_image, contour, approx):
    # print(contour.shape)
    # print(approx.shape)
    cv2.drawContours(output_image, [approx], -1, (255, 0, 0), 2)

    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    print(x, y, w, h)

    cv2.putText(output_image, str(w), (15, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(output_image, str(h), (95, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    roi_frame = original_image[y:(y + h), x:(x + w)]
    return roi_frame


def decode_barcode(original_image, roi_image):
    # Find barcodes and QR codes
    #
    img_yuv = cv2.cvtColor(roi_image, cv2.COLOR_BGR2YUV)

    # equalize the histogram of the Y channel
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])

    # convert the YUV image back to RGB format
    roi_image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    decoded_objects = pyzbar.decode(roi_image)

    # Print results
    for decoded_object in decoded_objects:
        # print('Type : ', decoded_object.type)
        # print('Data : ', decoded_object.data, '\n')
        cv2.putText(original_image, str(decoded_object.data) + ' (' + decoded_object.type + ')',
                    (15, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
