import cv2


class Toolbar:

    def __init__(self):

        self.height = 80

        self.tools = [

            ("Blue", (255, 0, 0)),
            ("Green", (0, 255, 0)),
            ("Red", (0, 0, 255)),
            ("Black", (0, 0, 0)),
            ("Yellow", (0, 255, 255)),
            ("Purple", (255, 0, 255)),
            ("Eraser", (255, 255, 255)),
            ("Clear", None),
            ("Save", None)

        ]

        self.selectedColor = (255, 0, 0)
        self.selectedName = "Blue"

    # --------------------------
    # Draw Toolbar
    # --------------------------
    def draw(self, frame):

        cv2.rectangle(
            frame,
            (0, 0),
            (1280, self.height),
            (230, 230, 230),
            -1
        )

        x = 20

        self.positions = []

        for name, color in self.tools:

            if color is not None:

                cv2.rectangle(
                    frame,
                    (x, 20),
                    (x + 40, 60),
                    color,
                    -1
                )

            else:

                cv2.rectangle(
                    frame,
                    (x, 20),
                    (x + 70, 60),
                    (180, 180, 180),
                    -1
                )

                cv2.putText(
                    frame,
                    name,
                    (x + 5, 47),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    2
                )

            width = 40 if color is not None else 70

            self.positions.append((x, x + width, name, color))

            x += width + 20

        return frame

    # --------------------------
    # Check Selection
    # --------------------------
    def checkSelection(self, x, y):

        if y > self.height:
            return None

        for left, right, name, color in self.positions:

            if left <= x <= right:

                if name == "Clear":
                    return ("CLEAR", None)

                if name == "Save":
                    return ("SAVE", None)

                self.selectedColor = color
                self.selectedName = name

                return ("COLOR", color)

        return None

    # --------------------------
    # Current Brush
    # --------------------------
    def showStatus(self, frame):

        cv2.putText(
            frame,
            f"Brush : {self.selectedName}",
            (900, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            self.selectedColor,
            2
        )