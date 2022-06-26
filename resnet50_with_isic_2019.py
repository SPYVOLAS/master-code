# -*- coding: utf-8 -*-
"""ResNet50 with ISIC 2019.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZFKRcMJojbgOhIs12KHt46U5U4Y13Clu
"""

from google.colab import drive
drive.mount('/content/drive')

#check if you are using a GPU session
import tensorflow as tf
tf.test.gpu_device_name()

# Commented out IPython magic to ensure Python compatibility.
#import necessary libraries
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import os
from glob import glob
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
from scipy import stats
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
# %matplotlib inline

import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import resnet
from keras.models import Sequential
import keras.layers as layers
from keras.layers import Conv2D, MaxPool2D, Dropout, Flatten, Dense, BatchNormalization
from keras.callbacks import ModelCheckpoint
import h5py
from tensorflow.keras.optimizers import Adam

#access the necessary files
metadata = pd.read_csv("/content/drive/MyDrive/ISIC_2019_Training_Metadata.csv")
ground_truth_data = pd.read_csv("/content/drive/MyDrive/ISIC_2019_Training_GroundTruth.csv")
data = "/content/drive/MyDrive/ISIC_2019_Training_Input"
train_data = "/content/drive/MyDrive/ISIC_2019_train"
validation_data = "/content/drive/MyDrive/ISIC_2019_val"
test_data = "/content/drive/MyDrive/ISIC_2019_test"
train_metadata = pd.read_csv("/content/drive/MyDrive/ISIC_2019_train_metadata.csv")
validation_metadata =pd.read_csv("/content/drive/MyDrive/ISIC_2019_val_metadata.csv")
test_metadata = pd.read_csv("/content/drive/MyDrive/ISIC_2019_test_metadata.csv")

plt.figure(figsize=(20,8))
sns.set(style="ticks", font_scale = 1)
ax = sns.countplot(data = metadata,x='age_approx',palette="Blues_d", hue = 'sex')
sns.despine(top=True, right=True, left=True, bottom=False)
plt.xticks(rotation=0,fontsize = 12)
ax.set_xlabel('Age',fontsize = 14,weight = 'bold')
ax.set_ylabel('Count',fontsize = 14,weight = 'bold')
plt.title('Age Distribution', fontsize = 16,weight = 'bold');

#plot the localization of lesions for ISIC 2019 cases
fig = plt.figure(figsize=(25,15))
ax1 = fig.add_subplot(221)
metadata["anatom_site_general"].value_counts().plot(kind = 'bar', color=["blue", "red", "green", "orange", "brown", "pink", "purple", "black"], ax = ax1)
ax1.set_ylabel('Count', fontsize=14, weight="bold")
ax1.set_xlabel('Localization of Skin Lesion', fontsize=14, weight = "bold")

#show one image from each class of ISIC 2019 dataset
fig = plt.figure(figsize=(12,5))

rows = 2
columns = 4

image1 = Image.open('/content/drive/MyDrive/ISIC_2019_Training_Input/ISIC_0000002 resized.jpg')
image2 = Image.open('/content/drive/MyDrive/ISIC_2019_Training_Input/ISIC_0000001 resized.jpg')
image3 = Image.open('/content/drive/MyDrive/ISIC_2019_Training_Input/ISIC_0024403 resized.jpg')
image4 = Image.open('/content/drive/MyDrive/ISIC_2019_Training_Input/ISIC_0025427 resized.jpg')
image5 = Image.open('/content/drive/MyDrive/ISIC_2019_Training_Input/ISIC_0010491 resized.jpg')
image6 = Image.open('/content/drive/MyDrive/ISIC_2019_Training_Input/ISIC_0026417 resized.jpg')
image7 = Image.open('/content/drive/MyDrive/ISIC_2019_Training_Input/ISIC_0025425 resized.jpg')
image8 = Image.open('/content/drive/MyDrive/ISIC_2019_Training_Input/ISIC_0024418 resized.jpg')


fig.add_subplot(rows, columns, 1)

plt.imshow(image1)
plt.axis('off')
plt.title("Melanoma")

fig.add_subplot(rows, columns, 2)

plt.imshow(image2)
plt.axis('off')
plt.title("Melanocytic nevi")

fig.add_subplot(rows, columns, 3)

plt.imshow(image3)
plt.axis('off')
plt.title("Basal cell carcinoma")

fig.add_subplot(rows, columns, 4)

plt.imshow(image4)
plt.axis('off')
plt.title("Aktinic keratosis")

fig.add_subplot(rows, columns, 5)

plt.imshow(image5)
plt.axis('off')
plt.title("Benign keratosis-like lesions")

fig.add_subplot(rows, columns, 6)

plt.imshow(image6)
plt.axis('off')
plt.title("Dermatofibroma")

fig.add_subplot(rows, columns, 7)

plt.imshow(image7)
plt.axis('off')
plt.title("Vascular lesion")

fig.add_subplot(rows, columns, 8)

plt.imshow(image8)
plt.axis('off')
plt.title("Squamus cell carcinoma")

#create generator for training data
train_datagen = ImageDataGenerator(
        rescale=1/255.0,
        shear_range=0.3,
        zoom_range=0.3,
        rotation_range=90)

train_generator = train_datagen.flow_from_directory(
        '/content/drive/MyDrive/ISIC_2019_train',
        batch_size=32,
        target_size = (227, 227),
        shuffle = True,
        class_mode='categorical')

#create generator for validation data
val_datagen = ImageDataGenerator(
        rescale=1/255.0,
        shear_range=0.3,
        zoom_range=0.3,
        rotation_range=90)

val_generator = val_datagen.flow_from_directory(
        '/content/drive/MyDrive/ISIC_2019_val',
        batch_size=10,
        shuffle = True,
        target_size = (227, 227),
        class_mode='categorical')

#create generator for testing data
test_datagen = ImageDataGenerator(rescale=1/255.0)

test_generator = test_datagen.flow_from_directory(
        '/content/drive/MyDrive/ISIC_2019_test',
        batch_size=1,
        target_size = (227, 227),
        class_mode='categorical')

#ResNet50 architecture
from keras.applications.resnet import ResNet50
model = Sequential()

model1.add(ResNet50(include_top=False, pooling='avg', input_shape=(227,227, 3), weights = 'imagenet'))
model1.add(Dropout(0.7))
model1.add(Dense(1024, activation='relu'))
model1.add(Dropout(0.7))
model1.add(Dense(512, activation='relu'))
model1.add(Dropout(0.7))
model1.add(Dense(256, activation='relu'))
model1.add(Dropout(0.7))
model1.add(Dense(8, activation='softmax'))

model1.layers[0].trainable = True

model1.summary()

from keras.callbacks import ModelCheckpoint
checkpoint1 = ModelCheckpoint("/content/drive/MyDrive/best_model_ResNet50.h5", monitor='val_acc', verbose=1,
    save_best_only=False, mode='max', save_freq="epoch")

optimizer = Adam(learning_rate=3e-4)
model1.compile(optimizer=optimizer,
              loss='categorical_crossentropy',
              metrics=['accuracy', "Recall", "Precision"]
            )

history = model1.fit(train_generator, validation_data = val_generator, epochs=25, callbacks=[checkpoint1])

score = model1.evaluate(test_generator)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print('Test Recall:', score[2])
print('Test Precision:', score[3])