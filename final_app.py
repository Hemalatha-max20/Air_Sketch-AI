import cv2
import mediapipe as mp
import time

from gesture import GestureDetector
from drawing import AirCanvas
from ui import Toolbar

# --------------------------------
# Camera
# --------------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# --------------------------------
# MediaPipe
# --------------------------------
mpHands = mp.solutions.hands

hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mpDraw = mp.solutions.drawing_utils

# --------------------------------
# Objects
# --------------------------------
gestureDetector = GestureDetector()
canvas = AirCanvas()
toolbar = Toolbar()

previousTime = 0

saveCooldown = 0
clearCooldown = 0

# --------------------------------
# Main Loop
# --------------------------------
while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    h, w, c = frame.shape

    gesture = "NONE"

    indexX = 0
    indexY = 0

    toolbar.draw(frame)

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        mpDraw.draw_landmarks(
            frame,
            hand,
            mpHands.HAND_CONNECTIONS
        )

        lmList = []

        for lm in hand.landmark:

            x = int(lm.x * w)
            y = int(lm.y * h)

            lmList.append((x, y))

        gesture = gestureDetector.getGesture(lmList)

        indexX, indexY = lmList[8]

        cv2.circle(
            frame,
            (indexX, indexY),
            10,
            (0, 0, 255),
            cv2.FILLED
        )

        # --------------------------
        # DRAW MODE
        # --------------------------

        if gesture == "DRAW":

            canvas.draw(indexX, indexY)

        else:

            canvas.reset()

        # --------------------------
        # SELECT MODE
        # --------------------------

        if gesture == "SELECT":

            result = toolbar.checkSelection(indexX, indexY)

            if result is not None:

                action, value = result

                if action == "COLOR":

                    canvas.setColor(value)

                elif action == "CLEAR":

                    if time.time() - clearCooldown > 1:

                        canvas.clear()
                        clearCooldown = time.time()

                elif action == "SAVE":

                    if time.time() - saveCooldown > 1:

                        filename = canvas.save()

                        print("Saved :", filename)

                        saveCooldown = time.time()
                            # --------------------------
    # Show Brush Status
    # --------------------------
    toolbar.showStatus(frame)

    # --------------------------
    # Show Gesture
    # --------------------------
    cv2.putText(
        frame,
        f"Gesture : {gesture}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    # --------------------------
    # FPS
    # --------------------------
    currentTime = time.time()

    fps = int(1 / (currentTime - previousTime)) if previousTime != 0 else 0

    previousTime = currentTime

    cv2.putText(
        frame,
        f"FPS : {fps}",
        (1100, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    # --------------------------
    # Merge Camera + Canvas
    # --------------------------
    output = canvas.overlay(frame)

    # --------------------------
    # Show Window
    # --------------------------
    cv2.imshow("AirSketch AI", output)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

# --------------------------------
# Cleanup
# --------------------------------
cap.release()
cv2.destroyAllWindows()