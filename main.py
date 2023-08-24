# Import necessary libraries
import os
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

# Function to load images from a folder and return a list of images
def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        img = cv.imread(os.path.join(folder_path, filename))
        if img is not None:
            images.append(img)
    return images

# Function to add black border to an image
def add_border_with_text(img, border_size, text):
    img_with_border = cv.copyMakeBorder(img, border_size, border_size, border_size, border_size, cv.BORDER_CONSTANT, value=(0, 0, 0))
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_thickness = 2
    text_size = cv.getTextSize(text, font, font_scale, font_thickness)[0]
    text_position = (border_size - 10, img.shape[0] + text_size[1] + 10)
    cv.rectangle(img_with_border, (0, img.shape[0]), (img_with_border.shape[1], img_with_border.shape[0] + text_size[1] + 10), (0, 0, 0), cv.FILLED)
    cv.putText(img_with_border, text, text_position, font, font_scale, (0, 255, 0), font_thickness, cv.LINE_AA)
    return img_with_border

# Initialize camera capture
cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load background image and mode images
imgBackground = cv.imread('Resources/Background.png')
listImgModes = load_images_from_folder('Resources/Modes')
listImgIcons = load_images_from_folder('Resources/Icons')
instruct = cv.imread("Resources/fingers.png")

# Precompute constant values
instruct = cv.resize(instruct, (160, 120))
instruct = add_border_with_text(instruct,  15, "Gesture Instruction")  # Add a black border of 5 pixels
instruct = cv.resize(instruct, (160, 120))  # Resize to fit the specified region
modePositions = [(1136, 196), (1000, 384), (1136, 584)]

# Initialize variables
modeType = 0
selection = -1
counter = 0
selectionSpeed = 10
counterPause = 0
selectionList = [-1, -1, -1]

# Create hand detector instance
handDetector = HandDetector(detectionCon=0.8, maxHands=1)

# Main loop to process video stream and hand gestures
while True:
    # Read frame from the camera
    _, frame = cap.read()

    # Find hands and their landmarks using HandDetector
    hands, img = handDetector.findHands(frame)

    # Overlay feed on the background
    imgBackground[139:139+480, 50:50+640] = frame
    imgBackground[0:720, 847:1280] = listImgModes[modeType]
    imgBackground[0:120, 680:840] = instruct

    # Check if hands are detected and mode selection is allowed
    if hands and counterPause == 0 and modeType < 3:
        hand1 = hands[0]
        fingers = handDetector.fingersUp(hand1)

        # Detect hand gestures for mode selection
        if fingers == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0

        # Update selection counter and check if the mode is selected
        if counter > 0:
            counter += 1
            cv.ellipse(imgBackground, modePositions[selection - 1], (103, 103), 0, 0, counter * selectionSpeed,
                       (0, 255, 0), 20)
            if counter * selectionSpeed > 360:
                selectionList[modeType] = selection
                counter = 0
                selection = -1
                counterPause = 1
                modeType += 1

    # Pause after selection is made
    if counterPause > 0:
        counterPause += 1

        if counterPause > 60:
            counterPause = 0

            # When modeType is greater than or equal to 3, reset modeType and selectionList
            if counterPause == 0 and modeType >= 3:
                counterPause = 0
                modeType = 0
                selectionList = [-1, -1, -1]

    # Add selected items at the bottom of the background
    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]

    # Display the captured frame and the modified background
    cv.imshow('Background', imgBackground)

    # Exit on pressing the 'q' key
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and destroy windows
cap.release()
cv.destroyAllWindows()
