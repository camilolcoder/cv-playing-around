# app.py
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time

st.set_page_config(page_title="Hand Expansion Visualizer", layout="wide")
st.title("🤚 Hand Expansion Visualizer")

# placeholders
video_slot   = st.empty()
progress_bar = st.progress(0)
direction    = st.empty()

# MediaPipe hands
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

# track previous aperture
prev_aperture = None

# expected raw range of thumb–index distance (you can tune these)
MIN_AP, MAX_AP = 0.0, 0.4

cap = cv2.VideoCapture(2)
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Cannot read from camera")
            break

        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res   = hands.process(rgb)

        # compute thumb–index distance
        aperture = 0.0
        if res.multi_hand_landmarks:
            hand = res.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            t = hand.landmark[4]   # thumb tip
            i = hand.landmark[8]   # index tip
            aperture = np.hypot(t.x - i.x, t.y - i.y)

        # normalize to 0–1
        norm = np.clip((aperture - MIN_AP) / (MAX_AP - MIN_AP), 0.0, 1.0)
        progress_bar.progress(int(norm * 100))

        # show expanding vs contracting
        if prev_aperture is not None:
            if aperture > prev_aperture:
                direction.markdown("🎈 **Expanding**")
            elif aperture < prev_aperture:
                direction.markdown("🪂 **Contracting**")
            else:
                direction.markdown("⚖️ **Stable**")
        prev_aperture = aperture

        # display camera frame
        video_slot.image(frame, channels="BGR")

        time.sleep(0.03)
finally:
    cap.release()
