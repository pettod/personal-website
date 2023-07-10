import cv2
import numpy as np


IMAGE_PATH = "assets/linkedin_logo.png"
BRIGHTNESS_CHANGE = 40


def changeBrightness(image, value):
    image_alpha = np.expand_dims(image[..., 3], axis=2)
    image = image[..., :3]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    if value > 0:
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
    else:
        v[v < value] = 0
        v[v >= lim] += value

    final_hsv = cv2.merge((h, s, v))
    image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return np.concatenate([image, image_alpha], axis=-1)


def main():
    image = cv2.imread(IMAGE_PATH, cv2.IMREAD_UNCHANGED)
    image = changeBrightness(image, BRIGHTNESS_CHANGE)
    cv2.imwrite("brightened_darkened_image.png", image)



main()
