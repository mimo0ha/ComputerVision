import cv2
import numpy as np
import mss
import pyautogui
import time

def detect_feature(screen, template):

    # Convert the screen to grayscale for processing
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)

    # Match the template
    result = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)

    # Get the best match position
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Set a threshold for detection
    threshold = 0.8  # Adjust as needed
    if max_val >= threshold:
        top_left = max_loc
        h, w = template.shape
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
        # Draw a rectangle around the detected feature
        cv2.rectangle(screen, top_left, bottom_right, (0, 255, 0), 2)

    return screen

def monitor_screen(template_path):
    # Load the template image in grayscale
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print("Error: Template image not found.")
        return

    with mss.mss() as sct:
        while True:
            # Capture the entire screen
            screen = np.array(sct.grab(sct.monitors[0]))

            # Process the screen to detect the feature
            screen_with_detection = detect_feature(screen, template)

            # Display the screen with detection
            cv2.imshow("Screen Capture with Detection", cv2.cvtColor(screen_with_detection, cv2.COLOR_BGRA2BGR))

            # Quit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

def main():
    # Path to the template image of the feature
    template_path = "k2.jpg"  # Replace with the path to your template image

    # Start monitoring the screen
    print("Starting screen capture. Press 'q' to quit.")
    monitor_screen(template_path)

if __name__ == "__main__":
    main()