import cv2
import roi


def process_and_detect(src, window_manager):
    height, width, channels = src.shape
    cropping = src[300:900, 500:width-500]

    # TODO: Image Processor
    processing = _image_processing_template_one(cropping, window_manager)
    # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # filtering = cv2.bilateralFilter(gray, 1, 10, 120)

    # TODO: Object Detector
    processing_output = cv2.cvtColor(processing, cv2.COLOR_GRAY2BGR)
    success_detect, contour, approx = _try_detect(
        input_image=processing, output_image=processing_output, window_manager=window_manager)

    roi_output = None
    if success_detect:
        # ROI
        roi_output = roi.post_detect(original_image=cropping, output_image=processing_output,
                                     contour=contour, approx=approx)
        roi.decode_barcode(original_image=cropping, roi_image=roi_output)
    else:
        # TODO: image_processing_template_two
        pass

    # TODO: to be continued
    return processing_output, roi_output


def _image_processing_template_one(src, window_manager):
    # TODO: Color space: GRAYSCALE, HSV, ...
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # TODO: Convolution, Blurring, ...
    # filtering = cv2.bilateralFilter(gray, 1, 10, 120)
    filtering = _image_filtering(gray, window_manager)

    # TODO: Edge detection
    # edges = cv2.Canny(gray, 10, 250)
    edges = _edge_detection(filtering, window_manager)

    # TODO: Morphological operations
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    # closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    closed = _morphological_transformations(edges, window_manager)
    return closed


def _image_filtering(src, window_manager):
    diameter = window_manager.get_trackbar_value('Diameter (bilateralFilter)')
    sigma_color = window_manager.get_trackbar_value('SigmaColor (bilateralFilter)')
    sigma_space = window_manager.get_trackbar_value('SigmaSpace (bilateralFilter)')
    filtering = cv2.bilateralFilter(src, diameter, sigma_color, sigma_space)
    return filtering


def _edge_detection(src, window_manager):
    threshold_min = window_manager.get_trackbar_value('Threshold min (Canny edge detection)')
    threshold_max = window_manager.get_trackbar_value('Threshold max (Canny edge detection)')
    edges = cv2.Canny(src, threshold_min, threshold_max)
    return edges


def _morphological_transformations(src, window_manager):
    kernel_size = window_manager.get_trackbar_value('Kernel size (morphological operation)')
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    closed = cv2.morphologyEx(src, cv2.MORPH_CLOSE, kernel)
    return closed


def _try_detect(input_image, output_image, window_manager):
    success_standard, contour, approx = _detect_standard_rects(input_image, output_image, window_manager)
    if not success_standard:
        # TODO: detect_rects_by_lines
        pass

    return success_standard, contour, approx


def _detect_standard_rects(input_image, output_image, window_manager):
    contour_area_points = window_manager.get_trackbar_value('Contour area min amount points (*1000)')
    # approx_edges_amount = self._windowManager.get_trackbar_value('Approx edges amount')
    approx_edges_amount = 4

    _, contours, h = cv2.findContours(input_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rects_count = 0
    finding_4contour_area = 0
    finding_4contour = None
    finding_appox = None
    for contour in contours:
        if cv2.contourArea(contour) > contour_area_points * 1000:
            arc_len = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.1 * arc_len, True)
            if len(approx) == approx_edges_amount:
                # Find 4contour with maximum area
                if cv2.contourArea(contour) > finding_4contour_area:
                    finding_4contour = contour
                    finding_appox = approx
                    finding_4contour_area = cv2.contourArea(finding_4contour)

                rects_count += 1

    return rects_count > 0, finding_4contour, finding_appox
