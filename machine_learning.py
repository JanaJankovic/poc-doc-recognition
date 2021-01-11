import cv2 as cv
import numpy as np
from tensorflow import keras
from tensorflow.keras import models, layers
import os
import random
import pickle
import preprocessing


numpy_img_data = 'npdata'
trained_model = 'model'
x_train_filename = "xtrain_"
y_train_filename = "ytrain_"
x_test_filename = "xtest_"
y_test_filename = "ytest_"
x_validate_filename = 'xvalidate_'
y_validate_filename = 'yvalidate_'
photo_base = 'predict_set'

size = 128
categories = ['melanoma', 'nevus', 'seborrheic_keratosis']

training = []
testing = []
validating = []


def save(X, y, X_path, y_path):
    pickle_out = open(X_path, "wb")
    pickle.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open(y_path, "wb")
    pickle.dump(y, pickle_out)
    pickle_out.close()


def load(path_X, path_y, size):
    print(path_X + " " + path_y + " " + str(size))
    pickle_in = open(path_X, "rb")
    X = pickle.load(pickle_in)

    pickle_in = open(path_y, "rb")
    y = pickle.load(pickle_in)

    X = np.array(X)
    y = np.array(y)
    return X, y


def append_data(dir, type, category):
    print(dir + " " + type + " " + str(category))
    try:
        for file in os.listdir(dir):
            img = cv.imread(os.path.join(dir, file))
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            if type == 'train':
                training.append([img, category])
            elif type == 'test':
                testing.append([img, category])
            elif type == 'valid':
                validating.append([img, category])
    except:
        print(os.path.join(dir, file))


def reload(size):
    for dir in os.listdir('dataset_size' + str(size)):
        for category in os.listdir(os.path.join('dataset_size' + str(size), dir)):
            append_data(os.path.join('dataset_size' + str(size), dir, category), dir,
                        categories.index(category))

    random.shuffle(training)
    random.shuffle(testing)
    random.shuffle(validating)

    x_training = []
    y_training = []
    x_testing = []
    y_testing = []
    x_validating = []
    y_validating = []

    for features, label in training:
        features = np.array(features).reshape(size, size, 3)
        x_training.append(features)
        y_training.append(label)

    for features, label in testing:
        features = np.array(features).reshape(size, size, 3)
        x_testing.append(features)
        y_testing.append(label)

    for features, label in validating:
        features = np.array(features).reshape(size, size, 3)
        x_validating.append(features)
        y_validating.append(label)

    x_training = np.array(x_training)
    y_training = np.array(y_training)
    x_testing = np.array(x_testing)
    y_testing = np.array(y_testing)
    x_validating = np.array(x_validating)
    y_validating = np.array(y_validating)

    if not os.path.isdir(numpy_img_data):
        os.mkdir(numpy_img_data)

    if not os.path.isdir(os.path.join(numpy_img_data, str(size))):
        os.mkdir(os.path.join(numpy_img_data, str(size)))

    ext = str(size) + ".pickle"
    path = os.path.join(numpy_img_data, str(size))

    save(x_training, y_training, path + "\\" + x_train_filename + ext, path + "\\" + y_train_filename + ext)
    save(x_testing, y_testing, path + "\\" + x_test_filename + ext, path + "\\" + y_test_filename + ext)
    save(x_validating, y_validating, path + "\\" + x_validate_filename + ext, path + "\\" + y_validate_filename + ext)


def load_model(path):
    model = models.load_model(path)
    return model


def make_prediction(model, image_path):
    if not os.path.isdir(photo_base):
        os.mkdir(photo_base)

    filepath = image_path.split("\\")

    preprocessing.resize_image(image_path, photo_base + "\\" + filepath[len(filepath) - 1],
                               size)

    img = cv.imread(photo_base + "\\" + filepath[len(filepath) - 1])
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    probability_model = models.Sequential([model, layers.Softmax()])
    prediction = probability_model.predict(np.array([img]) / 255)

    return np.argmax(prediction)


if __name__ == '__main__':
    dataset_path = os.path.join(numpy_img_data, str(size))
    if not os.path.isdir(dataset_path) or len(os.listdir(dataset_path)) == 0:
        reload(size)

    ext = str(size) + ".pickle"

    x_training, y_training = load(dataset_path + "\\" + x_train_filename + ext, dataset_path + "\\" + y_train_filename + ext,
                                  size)
    x_testing, y_testing = load(dataset_path + "\\" + x_test_filename + ext, dataset_path + "\\" + y_test_filename + ext,
                                size)
    x_validating, y_validating = load(dataset_path + "\\" + x_validate_filename + ext, dataset_path + "\\"
                                    + y_validate_filename + ext, size)

    print(str(len(x_training)) + " " + str(len(x_validating)) + " " + str(len(x_testing)))
    x_training = x_training / 255.0
    x_testing = x_testing / 255.0
    x_validating = x_validating / 255.0

    model_path = trained_model + '\\model_' + str(size) + '.model'

    if not os.path.isdir(model_path):
        print("Starting to learn")
        model = models.Sequential()
        model.add(layers.Conv2D(size, (3, 3), activation='relu', input_shape=(size, size, 3)))
        model.add(layers.MaxPool2D((2, 2)))
        model.add(layers.Conv2D(size, (3, 3), activation='relu'))
        model.add(layers.MaxPool2D((2, 2)))
        model.add(layers.Conv2D(size, (3, 3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(size, activation='relu'))
        model.add(layers.Dense(3, activation='softmax'))

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        cbs = [
            keras.callbacks.EarlyStopping(
                # Stop training when `val_loss` is no longer improving
                monitor='val_loss',
                # "no longer improving" being defined as "no better than 1e-2 less"
                min_delta=1e-2,
                # "no longer improving" being further defined as "for at least 2 epochs"
                patience=2,
                verbose=1)
        ]

        model.fit(x_training, y_training, epochs=10, validation_data=(x_validating, y_validating),
                  callbacks=cbs)

        if not os.path.isdir(trained_model) :
            os.mkdir(trained_model)

        model.save(model_path)

    else:
        print("Already learned")
        model = models.load_model(model_path)

    # predict_on_dataset_x = x_testing
    # predict_on_dataset_y = y_testing
    #
    # probability_model = models.Sequential([model, layers.Softmax()])
    # predictions = probability_model.predict(predict_on_dataset_x)
    #
    # confusion_matrix = np.zeros((3, 3), dtype=np.uint64)
    #
    # for i in range(len(predict_on_dataset_x)):
    #     prediction = predictions[i]
    #     confusion_matrix[np.argmax(prediction), predict_on_dataset_y[i]] += 1
    #
    # print(confusion_matrix)
    # loss, accuracy = model.evaluate(predict_on_dataset_x, predict_on_dataset_y)
    # print(f"Loss: {loss}")
    # print(f"Accuracy: {accuracy}")

    print (make_prediction(model, "C:\\Users\\Dell\\Desktop\\poc-doc-project\\poc-doc-recognition\\dataset_raw" +
                    "\\test\\melanoma\\ISIC_0012758.jpg"))
