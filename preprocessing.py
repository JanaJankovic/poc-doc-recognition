import cv2 as cv
import numpy as np
import os


def resize_image(source, destination, size):
    img = cv.imread(source)
    try:
        img = cv.resize(img, (size, size), interpolation=cv.INTER_AREA)
        cv.imwrite(destination, img)
    except:
        print(source)


if __name__ == '__main__':
    source_path = 'dataset_raw'
    size = 128
    destination_path = "dataset_size" + str(size)
    os.mkdir(destination_path)

    for dir in os.listdir(source_path):
        new_dir = destination_path + "\\" + dir
        os.mkdir(new_dir)
        for category in os.listdir(os.path.join(source_path, dir)):
            new_category = new_dir + "\\" + category
            os.mkdir(new_category)
            for file in os.listdir(os.path.join(source_path, dir, category)):
                source = source_path + "\\" + dir + "\\" + category + "\\" + file
                destination = new_category + "\\" + file
                resize_image(source, destination, size)
