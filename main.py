from game_window_detector import GameWindowDetector
from back_ground_processing import remove_background
import cv2


TEMPLATE_PATH = "k6.jpg"
detector = GameWindowDetector(template_path=TEMPLATE_PATH, threshold=0.5, monitor_index=1, scale_range=(0.5, 2.0),
                              scale_step=0.1)

detector.setup_monitor()

while True:
    # التقاط الشاشة
    screenshot = detector.capture_screen()
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # اكتشاف نافذة اللعبة
    if detector.game_window_coords is None:
        detector.game_window_coords = detector.detect_game_window(screenshot_gray)
        if detector.game_window_coords:
            print("Game window detected!")
        else:
            print("Game window not detected!")
            continue

    # استخراج نافذة اللعبة
    game_window = detector.extract_game_window(screenshot)

    if game_window is not None:
        # معالجة الإطار - إزالة الخلفية
        processed_frame = remove_background(game_window)

        # عرض الإطارين
        cv2.imshow("Original Game Stream", game_window)  # النافذة الأصلية
        cv2.imshow("Processed Game Stream (Background Removed)", processed_frame)  # النافذة المعالجة

    # كسر الحلقة عند الضغط على المفتاح 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

