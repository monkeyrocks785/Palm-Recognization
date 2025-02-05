import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()  
    
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    gesture_detected = False
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check if hand is a fists
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            
            # Calculate the center of the hand (palm)
            palm_center = ((index_tip.x + middle_tip.x + ring_tip.x + pinky_tip.x) / 4,
                           (index_tip.y + middle_tip.y + ring_tip.y + pinky_tip.y) / 4)

            # Fist Detection: All fingers should be curled
            if (index_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y and
                middle_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y and
                ring_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y and
                pinky_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y):
                cv2.putText(frame, "Fist Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Peace Sign Detection: Check if index and middle fingers are extended and separated
            if (index_tip.y < thumb_tip.y and middle_tip.y < thumb_tip.y and
                index_tip.x > thumb_tip.x and middle_tip.x > thumb_tip.x and
                ring_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y and
                pinky_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y and 
                abs(index_tip.x - middle_tip.x) > 0.1):  # Ensure there's a visible gap between fingers
                cv2.putText(frame, "Peace Sign Detected", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Open Hand Detection: Check if all five fingers are extended
            if (index_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
                middle_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and
                ring_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y and
                pinky_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y):
                cv2.putText(frame, "Open Hand Detected", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Pointing Gesture: Index finger extended and thumb folded
            if index_tip.y < thumb_tip.y and index_tip.x > thumb_tip.x:
                # Index is above thumb and pointing out
                if (thumb_tip.x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x):  # Check if thumb is folded
                    # Draw an interactive AR circle at the palm center
                    object_position = (int(palm_center[0] * frame.shape[1]), int(palm_center[1] * frame.shape[0]))
                    cv2.circle(frame, object_position, 20, (0, 255, 0), -1)
                    gesture_detected = True
                    cv2.putText(frame, "Pointing Gesture", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
            # If no gesture is detected, you can add a default AR element or simply leave the frame.
            if not gesture_detected:
                cv2.putText(frame, "Move your hand to interact!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow('AR Experience', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()