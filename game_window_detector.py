import cv2
import numpy as np
import mss
import time

class GameWindowDetector:
    def __init__(self, template_path, threshold=0.5, monitor_index=1, scale_range=(0.5, 2.0), scale_step=0.1):
        """
        Initialize the GameWindowDetector.
        :param template_path: Path to the template image.
        :param threshold: Matching threshold for template matching.
        :param monitor_index: Index of the monitor to capture (default is the primary monitor).
        :param scale_range: Range of scales to resize the template for matching (min_scale, max_scale).
        :param scale_step: Step size for scaling the template.
        """
        self.template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        self.template_gray = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)
        self.template_h, self.template_w = self.template_gray.shape
        self.threshold = threshold
        self.monitor_index = monitor_index
        self.scale_range = scale_range
        self.scale_step = scale_step
        self.monitor = None
        self.game_window_coords = None
        self.sct = mss.mss()

    def setup_monitor(self):
        """Setup the monitor to capture."""
        self.monitor = self.sct.monitors[self.monitor_index]

    def capture_screen(self):
        """
        Capture the screen using mss.
        :return: The captured screenshot in BGR format.
        """
        screenshot = np.array(self.sct.grab(self.monitor))
        return cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    def detect_game_window(self, screenshot_gray):
        """
        Detect the game window using multi-scale template matching.
        :param screenshot_gray: Grayscale screenshot of the screen.
        :return: Coordinates of the detected game window (top_left, bottom_right) or None.
        """
        best_match = None
        best_val = 0

        for scale in np.arange(self.scale_range[0], self.scale_range[1], self.scale_step):
            resized_template = cv2.resize(self.template_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
            resized_h, resized_w = resized_template.shape

            if resized_h > screenshot_gray.shape[0] or resized_w > screenshot_gray.shape[1]:
                continue

            result = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > best_val and max_val >= self.threshold:
                best_val = max_val
                best_match = (max_loc, (max_loc[0] + resized_w, max_loc[1] + resized_h))

        if best_match:
            print(f"Best match found with value: {best_val}")
            return best_match
        return None

    def extract_game_window(self, screenshot):
        """
        Extract the game window from the screenshot.
        :param screenshot: The full screenshot.
        :return: Cropped image of the game window.
        """
        if self.game_window_coords:
            top_left, bottom_right = self.game_window_coords
            return screenshot[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        return None

    def display_game_stream(self):
        """
        Main function to detect the game window and display the live stream.
        """
        self.setup_monitor()

        while True:
            screenshot = self.capture_screen()
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

            if self.game_window_coords is None:
                self.game_window_coords = self.detect_game_window(screenshot_gray)
                if self.game_window_coords:
                    print("Game window detected!")
                else:
                    print("Game window not detected!")
                    time.sleep(0.5)
                    continue

            game_window = self.extract_game_window(screenshot)
            if game_window is not None:
                cv2.imshow("Game Live Stream", game_window)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
