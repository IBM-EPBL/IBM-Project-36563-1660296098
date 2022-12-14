# -*- coding: utf-8 -*-
"""Images.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-wukQDc0bCqzKmDXuvpJGUD8xdvvQoMa
"""

import os
from playsound import playsound
import cv2 as cv
import numpy as np
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def Read_Image(filename):
    try:
        image = cv.imread(filename)
        image = np.uint8(image)
    except:
        print(filename)

    return image


directory_path = './dataset/Dataset/Dataset/'
listDir = os.listdir(directory_path)

Images = []
Target = []
for i in range(len(listDir)):
    folder = directory_path + listDir[i]
    listfold = os.listdir(folder)
    for j in range(len(listfold)):
        sub_folder = folder + '/' + listfold[j]
        sublist = os.listdir(sub_folder)
        for k in range(len(sublist)):
            print(i, j, k)
            filename = sub_folder + '/' + sublist[k]
            image = Read_Image(filename)
            Target.append(1 if 'fire' in listfold[j] else 0)
            Images.append(image)
np.save("Images.npy", Images)
np.save("Target.npy", Target)

train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

xtrain = train_datagen.flow_from_directory('./dataset/Dataset/Dataset/train_set',
                                           target_size=(64, 64),
                                           class_mode='categorical',
                                           batch_size=100)

xtest = test_datagen.flow_from_directory('./dataset/Dataset/Dataset/test_set',
                                         target_size=(64, 64),
                                         class_mode='categorical',
                                         batch_size=100)

model = Sequential()  # Initializing the model
model.add(Convolution2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))  # Covolution layer
model.add(MaxPooling2D(pool_size=(2, 2)))  # Max pooling layer
model.add(Flatten())  # Flatten layer
model.add(Dense(300, activation='relu'))  # Hidden layer 1
model.add(Dense(150, activation='relu'))  # Hidden layer 2
model.add(Dense(2, activation='softmax'))  # Output layer

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit_generator(xtrain,
                     steps_per_epoch=len(xtrain),
                     epochs=10,
                     validation_data=xtest,
                     validation_steps=len(xtest))

model.save('fire.h5')

img = cv.imread('./dataset/Dataset/Dataset/test_set/forest/1_chimp.jpg')  # Reading image
# x = image.img_to_array(img) # Converting image to array
x = cv.resize(img, (64, 64))
x = np.expand_dims(x, axis=0)  # Expanding dimension
pred = np.argmax(model.predict(x))  # Predicting higher prob. index
print(pred, model.predict(x))
op = ['fire', 'no fire']  # Creating list of output categories
print(op[pred])  # Matching the index

img = cv.imread('./dataset/Dataset/Dataset/test_set/forest/146019.jpg')  # Reading image
x = cv.resize(img, (64, 64))  # Converting image to array
x = np.expand_dims(x, axis=0)  # Expanding dimension
pred = np.argmax(model.predict(x))  # Predicting higher prob. index
print(pred, model.predict(x))
op = ['fire', 'no fire']  # Creating list of output categories
print(op[pred])  # Matching the index