import cv2
import mediapipe as mp
import pyautogui
import datetime
import threading
import keyboard
from playsound import playsound
import os

def detect_gesture_and_capture():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7)
    cap = cv2.VideoCapture(0)
    gesture_detected = False

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                h, w, _ = frame.shape
                x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
                x2, y2 = int(index_tip.x * w), int(index_tip.y * h)

                dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

                if dist < 30:
                    filename = datetime.datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
                    pyautogui.screenshot(filename)
                    print(f"📸 Saved: {filename}")
                    try:
                        playsound("shutter.mp3")  # Ensure this file exists or use os.system("echo \a")
                    except:
                        os.system("echo \a")
                    gesture_detected = True
                    break

        if gesture_detected:
            break

    cap.release()

def on_hotkey_triggered():
    threading.Thread(target=detect_gesture_and_capture, daemon=True).start()

# Register global hotkey (e.g., Ctrl+Alt+S)
keyboard.add_hotkey('alt+s', on_hotkey_triggered)

print("🟢 Gesture Screenshot App is running in background. Press Ctrl+Alt+S to trigger.")
keyboard.wait()  # Keeps app alive
