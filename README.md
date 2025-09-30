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

Install dependencies:

```bash
pip install -r requirements.txt
