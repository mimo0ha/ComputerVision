import cv2
import numpy as np
import mss
import pyautogui
import time


def find_game_window(template_path):
    """
    Captures the screen and finds the game window using template matching.
    """
    # Load the reference image
    tree_template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if tree_template is None:
        print("Reference image not found.")
        return None

    # Convert template to grayscale
    tree_template_gray = cv2.cvtColor(tree_template, cv2.COLOR_BGR2GRAY)

    # Capture the screen
    with mss.mss() as sct:
        screen = np.array(sct.grab(sct.monitors[0]))
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)

        # Perform template matching
        result = cv2.matchTemplate(screen_gray, tree_template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # Define a threshold
        threshold = 0.7
        if max_val >= threshold:
            print(f"Game window detected with confidence: {max_val}")
            h, w = tree_template_gray.shape
            return (max_loc[0], max_loc[1], max_loc[0] + w, max_loc[1] + h)
        else:
            print("Game window not detected.")
            return None


def monitor_game(bbox):
    """
    Monitor the game area and display it.
    """
    with mss.mss() as sct:
        while True:
            # Capture the defined area (game area)
            screen = np.array(sct.grab({
                "left": bbox[0],
                "top": bbox[1],
                "width": bbox[2] - bbox[0],
                "height": bbox[3] - bbox[1],
            }))

            # Display the captured area
            cv2.imshow("Game Screen", cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR))

            # Quit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


def main():
    # Path to the template image
    template_path = "karate kido2.png"

    # Find the game window
    bbox = find_game_window(template_path)

    if bbox:
        print(f"Game window found at: {bbox}")
        monitor_game(bbox)
    else:
        print("Game window not found.")


if __name__ == "__main__":
    main()
