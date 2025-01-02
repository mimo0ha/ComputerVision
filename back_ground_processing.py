import cv2
import numpy as np


def remove_background(frame):
    """
    Remove the background from a frame using color segmentation or other techniques.
    :param frame: Input frame (BGR image).
    :return: The frame with the background removed.
    """
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the color of interest (e.g., human body)
    lower_bound = np.array([10, 100, 100])  # Adjust these values as needed
    upper_bound = np.array([25, 255, 255])

    # Create a mask for the color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Refine the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Apply the mask to the input frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    return result
