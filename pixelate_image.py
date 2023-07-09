import cv2
import os
from tqdm import tqdm
import shutil


IMAGE_PATH = "assets/peter_todorov_profile.png"
OUTPUT_PATH = "pixelated_frames"
NUMBER_OF_FRAMES = 100
RESIZE_FACTOR = 1.05


def main():
    image = cv2.imread(IMAGE_PATH, cv2.IMREAD_UNCHANGED)
    h_org, w_org, c = image.shape
    if os.path.isdir(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    cv2.imwrite(f"{OUTPUT_PATH}/{NUMBER_OF_FRAMES}.png", image)
    for i in tqdm(range(NUMBER_OF_FRAMES)):
        h, w, c = image.shape
        image = cv2.resize(
            image,
            (
                int(w/RESIZE_FACTOR),
                int(h/RESIZE_FACTOR)
            ), interpolation=cv2.INTER_CUBIC)
        image_org_size = cv2.resize(image, (w_org, h_org), interpolation=cv2.INTER_NEAREST)
        os.makedirs(OUTPUT_PATH, exist_ok=True)
        cv2.imwrite(f"{OUTPUT_PATH}/{NUMBER_OF_FRAMES - 1 - i}.png", image_org_size)
        #cv2.imwrite(f"{OUTPUT_PATH}/{NUMBER_OF_FRAMES + 1 + i}.png", image_org_size)


main()
