import cv2
import numpy as np
import os
import shutil
from tqdm import tqdm


IMAGE_PATH = "assets/peter_todorov_profile.png"
OUTPUT_PATH = "pixelated_frames"
NUMBER_OF_FRAMES = 100
RESIZE_FACTOR = 1.05


def addNoise(image, mean, sigma, color_noise=True):
    gaussian_0 = 255 * np.random.normal(mean, sigma, (image.shape[0],image.shape[1]))
    if color_noise:
        gaussian_1 = 255 * np.random.normal(mean, sigma, (image.shape[0],image.shape[1]))
        gaussian_2 = 255 * np.random.normal(mean, sigma, (image.shape[0],image.shape[1]))
    else:
        gaussian_1 = gaussian_0
        gaussian_2 = gaussian_0
    gaussian = np.stack([
        gaussian_0,
        gaussian_1,
        gaussian_2,
        np.zeros((image.shape[0], image.shape[1]))
    ], axis=-1)
    image = image.astype(np.float64) + gaussian
    return image.clip(0, 255).astype(np.uint8)


def main():
    image = cv2.imread(IMAGE_PATH, cv2.IMREAD_UNCHANGED)
    h_org, w_org, c = image.shape
    if os.path.isdir(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    cv2.imwrite(f"{OUTPUT_PATH}/{NUMBER_OF_FRAMES}.png", image)

    # Pixelate
    for i in tqdm(range(NUMBER_OF_FRAMES)):
        h, w, c = image.shape
        image = cv2.resize(
            image,
            (
                int(w/RESIZE_FACTOR),
                int(h/RESIZE_FACTOR)
            ), interpolation=cv2.INTER_CUBIC)
        image = addNoise(image, 0, 0.05, True)
        image_org_size = cv2.resize(image, (w_org, h_org), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(f"{OUTPUT_PATH}/{NUMBER_OF_FRAMES - 1 - i}.png", image_org_size)

    # Add noise, keep the same resolution
    number_of_noisy_frames = NUMBER_OF_FRAMES // 5
    for i in tqdm(range(number_of_noisy_frames)):
        image = addNoise(image, 0, 0.1, True)
        image_org_size = cv2.resize(image, (w_org, h_org), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(f"{OUTPUT_PATH}/0_{number_of_noisy_frames - 1 - i}.png", image_org_size)


main()
