# import cv2

# for i in [0, 1]:  # Try both indexes
#     cap = cv2.VideoCapture(i)
#     if cap.isOpened():
#         print(f"Trying camera index {i}...")
#         ret, frame = cap.read()
#         if ret:
#             cv2.imshow(f"Camera Index {i}", frame)
#             cv2.waitKey(3000)  # Show frame for 3 seconds
#             cv2.destroyAllWindows()
#         cap.release()


import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Try CAP_MSMF if CAP_DSHOW doesn't work

if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    cv2.imshow("AR Experience", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
