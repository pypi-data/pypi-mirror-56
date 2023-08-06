import argparse
import math
import numpy as np
import pickle
import random

from PIL import Image
from pathlib import Path


def unpickle(file):
    with open(file, 'rb') as fo:
        dataset = pickle.load(fo, encoding='bytes')
    return dataset


def overlay_images(path_to_cifar_100, path_to_sim):
    path_to_floor_texture = Path(
        path_to_sim).parents[0] / "worlds" / "carolo_transparent.png"
    floor_texture = Image.open(path_to_floor_texture)
    background = Image.fromarray(
        np.zeros(floor_texture.size + (3, )),
        mode="RGB",
    )

    dataset = unpickle(path_to_cifar_100)
    imgs = dataset[b"data"]
    n_imgs = imgs.shape[0]

    for i in range(math.ceil(floor_texture.width / 32)):
        for j in range(math.ceil(floor_texture.height / 32)):
            img = Image.fromarray(
                np.reshape(imgs[random.randrange(n_imgs)], (32, 32, 3), "F"),
                mode="RGB",
            )
            background.paste(img, (i * 32, j * 32))

    background.paste(floor_texture, (0, 0), floor_texture)
    path_to_overlayed = Path(
        path_to_sim).parents[0] / "worlds" / "carolo_overlayed.png"
    background.save(path_to_overlayed, "PNG")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_cifar_100", type=str)
    parser.add_argument("path_to_sim", type=str)
    args = parser.parse_args()
    return args.path_to_cifar_100, args.path_to_sim


if __name__ == "__main__":
    path_to_cifar_100, path_to_sim = parse_args()
    overlay_images(path_to_cifar_100, path_to_sim)
