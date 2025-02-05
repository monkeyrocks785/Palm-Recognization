import cv2

for i in range(5):  # Try different camera indexes
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera found at index {i}")
        cap.release()
