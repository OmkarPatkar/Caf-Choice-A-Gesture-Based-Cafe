# CafeChoice-A-Gesture-Based-Cafe
Gesture-Based coffee Selection with OpenCV and Hand Tracking

This project demonstrates a simple gesture-based mode selection application using OpenCV and Hand Tracking. The program allows users to interactively switch between different modes by using hand gestures, providing an intuitive and hands-free mode selection experience.

**Requirements:**

- Python 3.x
- OpenCV (cv2)
- cvzone (HandTrackingModule)

**Installation:**

- Clone or download this repository to your local machine.
- Install the required libraries by running: **pip install opencv-python cvzone**

**Usage:**

- Run the main.py script.
- The application will open the camera feed, and the background with mode options will be displayed.
- Use hand gestures to select modes:
- One finger up: Point with one finger to select the first mode.
- Two fingers up: Make a "V" shape with two fingers to select the second mode.
- Three fingers up: Make a "W" shape with three fingers to select the third mode.
- The application will show the progress of mode selection with an ellipse around the selected mode icon.
- Once the mode is fully selected, it will be displayed at the bottom of the background.
- After selecting all three modes, the application will reset the selection and go back to Mode 1 automatically.
- Exit the system by pressing the 'q' key.

**Folder Structure:**

- main.py: The main Python script for the gesture-based mode selection.
- Resources/
  - Background.png: The background image where the camera feed and mode icons are overlaid.
  - Modes/: Folder containing images for different modes.
  - Icons/: Folder containing icon images for selected modes.
  - fingers.png: Image with instructions for hand gestures.

**Customization:**

- If you want to add more modes, simply add mode images in the Modes folder and update the modePositions list in the script accordingly.
- To use different icons for the selected modes, add icon images in the Icons folder and modify the selection positions in the script.

**Credits:**

- This project uses the cvzone library's HandTrackingModule for hand tracking and gesture detection. Credit goes to cvzone for their contribution to computer vision. 


The project concept is based on cvzone, although some modifications have been made to the code to align with specific requirements and enhancements.


