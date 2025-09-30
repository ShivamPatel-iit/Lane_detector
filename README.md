# Lane Detector

Real-time lane detection using Python and OpenCV. This project detects lane lines from a webcam or video feed and highlights them in green.

## Features
- Detects lanes in real-time using OpenCV
- Applies edge detection, region-of-interest cropping, and Hough Line Transform
- Safe handling of missing or incomplete lane lines
- Auto-reconnects webcam if disconnected
- Configurable Canny thresholds and ROI

## Requirements
- Python 3.10+
- OpenCV (`opencv-python`)
- NumPy (`numpy`)
## How It Works

This project captures a live video feed from a webcam and detects lane lines on the road in real-time. The main steps are:

1. **Capture Video**: The program accesses the webcam and continuously reads frames.
2. **Preprocessing**: Each frame is converted to grayscale and blurred using Gaussian Blur to reduce noise.
3. **Edge Detection**: Canny edge detection highlights the edges in the frame.
4. **Region of Interest (ROI)**: Only the bottom half of the frame (where the lanes appear) is processed to reduce noise.
5. **Line Detection**: Hough Line Transform detects line segments representing lane lines.
6. **Line Averaging**: Detected lines are classified as left or right lanes and averaged using slope-intercept calculations to produce smooth lane lines.
7. **Display**: The final lane lines are drawn over the original video frame in green, showing the detected lanes in real-time.
8. **Stability Features**: The program handles missing lane lines, skips invalid detections, and auto-reconnects the webcam if it disconnects.

💡 **Outcome:**  
When you run the program, you will see a live video with **green lines over the road lanes**. It works best on straight lanes with clear markings and under good lighting conditions.

Install dependencies:

```bash
pip install -r requirements.txt
