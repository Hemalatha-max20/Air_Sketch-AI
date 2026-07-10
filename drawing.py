import cv2
import numpy as np


class AirCanvas:

    def __init__(self, width=1280, height=720):

        self.width = width
        self.height = height

        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)

        self.previousX = None
        self.previousY = None

        self.brushColor = (255, 0, 0)
        self.brushThickness = 6

    # ----------------------------
    # Change Brush Color
    # ----------------------------
    def setColor(self, color):
        self.brushColor = color

    # ----------------------------
    # Change Brush Size
    # ----------------------------
    def setThickness(self, thickness):
        self.brushThickness = thickness

    # ----------------------------
    # Draw
    # ----------------------------
    def draw(self, x, y):

        if self.previousX is None:
            self.previousX = x
            self.previousY = y

        cv2.line(
            self.canvas,
            (self.previousX, self.previousY),
            (x, y),
            self.brushColor,
            self.brushThickness
        )

        self.previousX = x
        self.previousY = y

    # ----------------------------
    # Stop Drawing
    # ----------------------------
    def reset(self):

        self.previousX = None
        self.previousY = None

    # ----------------------------
    # Clear Canvas
    # ----------------------------
    def clear(self):

        self.canvas[:] = 0

    # ----------------------------
    # Save Image
    # ----------------------------
    def save(self):

        filename = "AirSketch_Drawing.png"

        cv2.imwrite(filename, self.canvas)

        return filename

    # ----------------------------
    # Overlay Canvas
    # ----------------------------
    def overlay(self, frame):

        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)

        _, mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

        mask_inv = cv2.bitwise_not(mask)

        frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)

        canvas_fg = cv2.bitwise_and(
            self.canvas,
            self.canvas,
            mask=mask
        )

        return cv2.add(frame_bg, canvas_fg)