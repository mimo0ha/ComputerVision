from game_window_detector import GameWindowDetector
from back_ground_processing import remove_background
import cv2


def apply_thresholding(frame, threshold_value=127):
    """
    Apply thresholding to a frame.
    :param frame: Input frame (grayscale image).
    :param threshold_value: Threshold value for binary thresholding.
    :return: Thresholded frame.
    """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresholded_frame = cv2.threshold(gray_frame, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded_frame


def main():
    TEMPLATE_PATH = "k6.jpg"
    detector = GameWindowDetector(template_path=TEMPLATE_PATH, threshold=0.5, monitor_index=1, scale_range=(0.5, 2.0),
                                  scale_step=0.1)

    detector.setup_monitor()

    while True:
        screenshot = detector.capture_screen()
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        if detector.game_window_coords is None:
            detector.game_window_coords = detector.detect_game_window(screenshot_gray)
            if detector.game_window_coords:
                print("Game window detected!")
            else:
                print("Game window not detected!")
                continue

        # استخراج النافذة
        game_window = detector.extract_game_window(screenshot)

        if game_window is not None:
            # معالجة الإطار - إزالة الخلفية
            processed_frame = remove_background(game_window)

            # تطبيق عملية thresholding
            thresholded_frame = apply_thresholding(game_window)

            # عرض النافذتين
            cv2.imshow("Processed Game Stream (Background Removed)", processed_frame)
            cv2.imshow("Thresholded Game Stream", thresholded_frame)

        # كسر الحلقة عند الضغط على المفتاح 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
