import math


class GestureDetector:

    def __init__(self):
        pass

    def distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def fingersUp(self, lmList):

        if len(lmList) == 0:
            return None

        fingers = {}

        fingers["index"] = lmList[8][1] < lmList[6][1]
        fingers["middle"] = lmList[12][1] < lmList[10][1]
        fingers["ring"] = lmList[16][1] < lmList[14][1]
        fingers["pinky"] = lmList[20][1] < lmList[18][1]

        thumbDistance = self.distance(lmList[4], lmList[5])

        fingers["thumb"] = thumbDistance > 40

        return fingers

    def getGesture(self, lmList):

        fingers = self.fingersUp(lmList)

        if fingers is None:
            return "NONE"

        index = fingers["index"]
        middle = fingers["middle"]
        ring = fingers["ring"]
        pinky = fingers["pinky"]
        thumb = fingers["thumb"]

        if index and not middle and not ring and not pinky:
            return "DRAW"

        if index and middle and not ring and not pinky:
            return "SELECT"

        if thumb and not index and not middle and not ring and not pinky:
            return "SAVE"

        if index and middle and ring and pinky:
            return "CLEAR"

        if not thumb and not index and not middle and not ring and not pinky:
            return "STOP"

        return "NONE"