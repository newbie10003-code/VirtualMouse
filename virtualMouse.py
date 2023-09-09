# import cv2
# import numpy as np
# import mediapipe as mp
# import handTrackingModule as htm
# import time
# import autopy
# import matplotlib.pyplot as plt

# # Variables
wCam, hCam = 640, 480

# cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)

# image = cap.read()
# plt.imshow(np.array(image[1]))
# cv2.imshow("Image", np.array(image[1]))
# pTime = 0
# # cv2.waitKey(0)

# detector = htm.handDetector(maxHands = 1)

# while True:
#     # 1. Find hand landmarks
#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList, bbox = detector.findPosition(img)

#     # 2. Get the tip of the index and middle fingers

#     # If the index finger is up, the program will function as a mouse pointer
#     # Else if both index finger and middle finger are up, the program will function as a mouse clicker. When the fingers are certain point near to each other, the program will click.

#     # 3. Check which fingers are up

#     # 4. Only index finger : Moving mode

#     # 5. Convert coordinates to get the correct position of the mouse pointer

#     # 6. Smoothen values - So that the mouse pointer doesn't move abruptly or jitter

#     # 7. Move mouse

#     # 8. Both index and middle fingers are up : Clicking mode

#     # 9. Find distance between fingers

#     # 10. Click mouse if distance short

#     # 11. Frame rate
    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime
    # cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 5)

#     # 12. Display
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)


import cv2
import mediapipe as mp
import time
import pyautogui

pTime = 0
detector = mp.solutions.hands.Hands()
# detector.bounding_box()
drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
# cap.set(3, 1920)
# cap.set(4, 1080)
screenWidth, screenHeight = pyautogui.size()
index_y = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    # This is done because the hands module requires images to be in RGB color scheme
    
    # Get the shape of the frame
    frameHeight, frameWidth, _ = img.shape
    # print(frameHeight, frameWidth)

    results = detector.process(img)
    hands = results.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing.draw_landmarks(img, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frameWidth)
                y = int(landmark.y * frameHeight)
                # print(id, x, y)
                if id == 8:
                    # print("Hello")
                    cv2.circle(img = img, center = (x, y), radius = 20, color = (0, 255, 255))
                    index_x = screenWidth / frameWidth * x
                    index_y = screenHeight / frameHeight * y
                    pyautogui.moveTo(index_x, index_y)
                    # print(abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 20:
                        # print("Click")
                        pyautogui.click()
                        pyautogui.sleep(1)
                
                if id == 4:
                    # print("Hello")
                    cv2.circle(img = img, center = (x, y), radius = 20, color = (0, 255, 255))
                    thumb_x = screenWidth / frameWidth * x
                    thumb_y = screenHeight / frameHeight * y


    # hands_box = detector.bounding_box()
    # print(hands)

    # Show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)