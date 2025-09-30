import cv2
import numpy as np
import time

# ------------------ Lane Detection Functions ------------------ #

def region_of_interest(img):
    height = img.shape[0]
    width = img.shape[1]
    # Cover bottom half of the frame
    polygons = np.array([[
        (0, height),
        (width, height),
        (width, int(height*0.5)),
        (0, int(height*0.5))
    ]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, polygons, 255)
    return cv2.bitwise_and(img, mask)

def display_lines(img, lines):
    line_image = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            if line is None:
                continue
            try:
                x1, y1, x2, y2 = line
                # Skip invalid coordinates
                if any(v is None or np.isnan(v) for v in [x1, y1, x2, y2]):
                    continue
                cv2.line(line_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 5)
            except:
                continue
    return cv2.addWeighted(img, 0.8, line_image, 1, 1)

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    if lines is None:
        return None

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_line = make_coordinates(image, np.average(left_fit, axis=0)) if left_fit else None
    right_line = make_coordinates(image, np.average(right_fit, axis=0)) if right_fit else None

    lines_out = []
    if left_line is not None:
        lines_out.append(left_line)
    if right_line is not None:
        lines_out.append(right_line)

    if len(lines_out) == 0:
        return None
    return np.array(lines_out)

# ------------------ Main Video Loop ------------------ #

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW more stable on Windows
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        # Camera disconnected, try reconnecting
        cap.release()
        time.sleep(1)
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        continue

    # Convert to grayscale and detect edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 30, 120)  # lower thresholds for webcam
    cropped_edges = region_of_interest(edges)

    # Detect lines with Hough Transform
    lines = cv2.HoughLinesP(
        cropped_edges,
        2,
        np.pi/180,
        50,            # lower threshold to detect more lines
        np.array([]),
        minLineLength=20,
        maxLineGap=10
    )

    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)

    cv2.imshow("Lane Detection", line_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
