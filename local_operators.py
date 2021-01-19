from builtins import range

import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import os
import machine_learning
from PIL import Image


filepath = 'predict_set'
modelpath = 'model'

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) - 1) # + 1 or more, to show more colors
    # print(numLabels)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    # print((hist, _))
    hist = hist.astype("float")
    # print(hist)
    hist /= hist.sum()
    # print(hist)

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # #plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        ## print(color.astype("uint8").tolist())
        startX = endX

    # #return the bar chart
    return bar

def plotImg(img):
    if len(img.shape) == 2:
        plt.imshow(img, cmap='gray')
        plt.show()
    else:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()


def locate_object(picture_path, photo_saved_location, model_path, size, predicted_save_location):
    img = cv2.imread(picture_path)

    if not os.path.isdir(photo_saved_location):
        os.mkdir(photo_saved_location)

    path = picture_path.split("\\")
    filename = path[len(path) - 1]

    # img = cv2.imread('dataset_size128\\train\\nevus\\ISIC_0012891.jpg') #first one
    # img = cv2.imread('dataset_size128\\train\\nevus\\ISIC_0012680.jpg') #good
    # img = cv2.imread('dataset_size128\\train\\nevus\\ISIC_0013676.jpg') #fifth one
    # img = cv2.imread('dataset_size128\\train\\nevus\\ISIC_0013792.jpg') #second one

    image = img.copy()

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 131, 15)
    # plotImg(img)
    # plotImg(image)   =============================================================================<<<<<<<<<<<<<<<
    # plotImg(binary_img)
    _, _, boxes, _ = cv2.connectedComponentsWithStats(binary_img)

    boxes = boxes[1:]
    filtered_boxes = []
    for x,y,w,h,pixels in boxes:
        if pixels < 10000 and h < 200 and w < 200 and h > 10 and w > 10:
            filtered_boxes.append((x,y,w,h))
            # print(x, y, w, h)


    # #find and store rectangles
    rectangle_arr = []
    for x,y,w,h in filtered_boxes:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 1)
        # plotImg(cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),1))
        crop_img = img[(y+1):y + h, (x+1):x + w]
        # print(x, y, w, h) # coordinates
        # cv2.imshow("cropped", crop_img)
        # cv2.waitKey(0)
        rectangle_arr.append((crop_img, [], [x, y, w, h]))

    # plotImg(img)
    # plotImg(image)

    # for x in rectangle_arr:
    #     print(x[2][1])

    # for x in rectangle_arr:
    #     cv2.imshow("cropped", x[0])
    #     cv2.waitKey(0)
    #     print(x[1])

    # #add color rgb value to array
    for x in rectangle_arr:
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        ##show rectangles
        img = cv2.cvtColor(x[0], cv2.COLOR_BGR2RGB)
        # plt.imshow(img)
        # plt.show()

        img = img.reshape((img.shape[0] * img.shape[1],3)) ##represent as row*column,channel number
        clt = KMeans(n_clusters=3) ##cluster number
        clt.fit(img)

        hist = find_histogram(clt)

        for (percent, color) in zip(hist, clt.cluster_centers_):
            # #plot the relative percentage of each cluster
            # print(color.astype("uint8").tolist())
            x[1].append(color.astype("uint8").tolist())


    min = 765
    temp_arr = []
    index = 0
    r = 0
    g = 0
    b = 0
    # print(len(rectangle_arr))
    if len(rectangle_arr) > 1:
        for i in rectangle_arr:
            # print(i[1])
            for k in i[1]:
                # print(k)
                for y in k:
                    # print(y)
                    if k.index(y) == 0:
                        r = y
                    elif k.index(y) == 1:
                        g = y
                    elif k.index(y) == 2:
                        b = y
                # print(r, g, b)
                temp_arr.append([r, g, b, index])
                r = 0
                g = 0
                b = 0
            index += 1

    # print(temp_arr)

    min_count = 0
    min_r = 300
    min_g = 300
    min_b = 300

    for q in range(len(temp_arr)):
        if min_r > temp_arr[q][0]:
            min_count += 1
        if min_g > temp_arr[q][1]:
            min_count += 1
        if min_b > temp_arr[q][2]:
            min_count += 1
        if min_count == 2 or min_count == 3:
            min_r = temp_arr[q][0]
            min_g = temp_arr[q][1]
            min_b = temp_arr[q][2]
            min_count = 0
            index = temp_arr[q][3]
            continue

    ## show result
    # print(min_r, min_g, min_b)
    # print("result is: ", index)
    # print(rectangle_arr[index][2]) # coordinates

    x = rectangle_arr[index][2][0]
    y = rectangle_arr[index][2][1]
    w = rectangle_arr[index][2][2]
    h = rectangle_arr[index][2][3]


    ## final result without nametag
    # plotImg(cv2.rectangle(image, (x-3,y-8), (x+w+3,y+h+3), (198, 201, 95), 1)) #this one =============================================================================<<<<<<<<<<<<<<<
    temp_img = cv2.rectangle(image, (x-3,y-8), (x+w+3,y+h+3), (198, 201, 95), 1).copy()
    # cv2.rectangle(image, (x-3,y-8), (x+w+3,y+h+3), (0,255,0), 1)
    # plt.imshow(image)
    # plt.show()
    # plotImg(image)

    image = cv2.cvtColor(rectangle_arr[index][0], cv2.COLOR_BGR2RGB)
    # plt.imshow(image)
    # plt.show()
    cv2.imwrite(os.path.join(photo_saved_location, filename), image)

    model = machine_learning.load_model(model_path + "\\model_" + str(size) + ".model")
    category_index =  machine_learning.make_prediction(model, picture_path)

    category = machine_learning.categories[category_index]
    print(category)

    ##print final result
    font_size = 0.4
    text_result = ""
    if category=="seborrheic_keratosis":
        font_size = 0.24
        text_result = "Seborrheic keratosis"
    elif category=="nevus":
        text_result = "Nevus"
    elif category=="melanoma":
        text_result = "Melanoma"


    font = cv2.FONT_ITALIC
    cv2.putText(temp_img, text_result, (x - 4, y - 10), font, font_size, (0, 0, 0), 1, cv2.LINE_AA)
    # plotImg(temp_img) =============================================================================<<<<<<<<<<<<<<<

    if not os.path.isdir(predicted_save_location):
        os.mkdir(predicted_save_location)

    cv2.imwrite(os.path.join(predicted_save_location, filename), temp_img)
    return os.path.join(predicted_save_location, filename), text_result


locate_object('dataset_size128\\train\\nevus\\ISIC_0012680.jpg', "predict_set", "model", 128, "predicted_set")
