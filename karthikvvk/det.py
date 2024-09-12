import cv2 as cv
import numpy, matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models

(trimg, trlab), (teimg, telab) = datasets.cifar10.load_data()
trimg, teimg = trimg/255, teimg/225

class_names = ["plane", "car", "cat", "dog", "ship", "truck", "bird", "horse", "deer", "frog"]

for i in range(16):
    try:
        plt.subplot(4,4,i+1)
        plt.xticks()
        plt.yticks()
        plt.imshow(trimg[i], cmap=plt.cm.binary)
        plt.xlabel(class_names[trlab[i][0]])
    except:
        pass
plt.show()


trimg = trimg[:20000]
trlab = trlab[:20000]

teimg = teimg[:2000]
telab = telab[:2000]


model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation="relu", input_shape=(32,32,3)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3,3), activation="relu"))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3,3), activation="relu"))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation="relu"))
model.add(layers.Dense(10, activation="softmax"))

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(trimg, trlab, epochs=15, validation_data=(teimg, telab))