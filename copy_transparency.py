import cv2

FROM_IMAGE_PATH = "assets/pt_icon_light.png"
TO_IMAGE_PATH = "assets/pt_icon_dark_big.png"


def main():
    image_from = cv2.imread(FROM_IMAGE_PATH, cv2.IMREAD_UNCHANGED)
    image_to = cv2.imread(TO_IMAGE_PATH, cv2.IMREAD_UNCHANGED)
    image_to[..., 3] = image_from[..., 3]
    cv2.imwrite(f"{TO_IMAGE_PATH[:-4]}_transparency-copied.png", image_to)



main()
