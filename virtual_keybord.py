import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import cvzone
import math 
from pynput.keyboard import Controller

# Initialize the webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize the hand detector
detector = HandDetector(detectionCon=0.8)

# Define the layout of the keyboard buttons
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""
keyboard = Controller()

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (250, 0, 250), cv2.FILLED)
        cv2.putText(img, button.text, (x + 22, y + 63), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

#
# def drawAll(img, buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#         x, y = button.pos
#         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
#                           20, rt=0)
#         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
#                       (255, 0, 255), cv2.FILLED)
#         cv2.putText(imgNew, button.text, (x + 40, y + 60),
#                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#
#     out = img.copy()
#     alpha = 0.5
#     mask = imgNew.astype(bool)
#     print(mask.shape)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
#     return out


# Define a class for keyboard buttons
class Button():
    def __init__(self, pos, text, size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text

# Create a list of Button objects for each key
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 15, 100 * i + 50], key))


# Main loop
while True:
    # Capture a frame from the webcam
    success, img = cap.read()
    
    # Find hands in the frame using the detector
    hands, img = detector.findHands(img)
    lmList = hands[0]['lmList'] if hands else []
    
    # Draw the keyboard buttons on the frame
    img = drawAll(img, buttonList)

    # Check if a hand is detected
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # Check if the fingertip is within a button's bounding box
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                # Highlight the button
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 22, y + 63), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                
                # Get thumb tip and fingertip positions
                thumb_tip = lmList[4]
                fingertip = lmList[8]
                x1, y1 = thumb_tip[1], thumb_tip[2]
                x2, y2 = fingertip[1], fingertip[2]
                
                # Calculate distance between thumb tip and fingertip
                l = int(math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1))))

                print(l)

                # If distance is small, simulate key press
                if l < 25:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 22, y + 63), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    
                    # Update the text that's being typed
                    finalText += button.text
                    sleep(0.5)
    
    # Display the typed text
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    
    # Show the image with the drawn elements
    cv2.imshow('Image', img)
    cv2.waitKey(1)
