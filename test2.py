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
    threshold = 0.9  # Adjust as needed
    if max_val >= threshold:
        top_left = max_loc
        h, w = template.shape
        bottom_right = (top_left[0] + w, top_left[1] + h)
        return True, top_left, bottom_right

    return False, None, None

def monitor_screen(template_path):

    # Load the template image in grayscale
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print("Error: Template image not found.")
        return

    with mss.mss() as sct:
        # Initial screen capture to check for the feature
        screen = np.array(sct.grab(sct.monitors[0]))
        feature_found, top_left, bottom_right = detect_feature(screen, template)

        if not feature_found:
            print("Error: Game window not found on the initial screen. Exiting.")
            return

        # Calculate the region of interest (ROI)
        roi = {
            "left": top_left[0],
            "top": max(0, top_left[1] - 800),  # Extend upwards by 500 pixels, ensuring no negative values
            "width": bottom_right[0] - top_left[0],
            "height": bottom_right[1] - max(0, top_left[1] - 800),
        }

        print("Feature found! Focusing on the game window...")

        while True:
            # Capture only the ROI
            screen = np.array(sct.grab(roi))

            # Convert the screen to BGR for display
            screen_bgr = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

            # Resize the screen for display (adjust width and height as needed)
            width = 800
            height = int(800 * screen_bgr.shape[0] / screen_bgr.shape[1])  # Keep aspect ratio
            resized_screen = cv2.resize(screen_bgr, (width, height))

            # Display the screen
            cv2.imshow("Game Window Capture", resized_screen)

            # Quit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

def main():
    # Path to the template image of the feature
    template_path = "k3.jpg"  # Replace with the path to your template image

    # Start monitoring the screen
    print("Starting screen capture. Press 'q' to quit.")
    monitor_screen(template_path)

if __name__ == "__main__":
    main()
