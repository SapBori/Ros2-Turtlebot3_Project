# TensorFlow and tf.keras
from audioop import bias
from unittest.loader import VALID_MODULE_NAME
import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
import numpy as np

import matplotlib.pyplot as plt

TRAINING_DIR ="/home/kw2018741008/Deep/Arrow photo/train_set"
VALIDATION_DIR ="/home/kw2018741008/Deep/Arrow photo/test_set"

batch_size = 8
training_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    width_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    brightness_range=(0.5,1.3),
    horizontal_flip=False,
    fill_mode='nearest',
)

validation_datagen = ImageDataGenerator(rescale = 1./255)

train_generator = training_datagen.flow_from_directory(
    VALIDATION_DIR,
    batch_size=batch_size,
    target_size=(224,224),
    class_mode='categorical',
    shuffle=True
)
validation_generator = validation_datagen.flow_from_directory(
    VALIDATION_DIR,
    batch_size=batch_size,
    target_size=(224,224),
    class_mode='categorical',
)

img, label = next(train_generator)
plt.figure(figsize=(20,20))

for i in range(8):
    plt.subplot(3,3,i+1)
    plt.imshow(img[i])
    plt.title(label[i])
    plt.axis('off')

plt.show()


# Load pre-trained base model.
base_model = tf.keras.applications.VGG16(input_shape=(224, 224, 3),
                                               include_top=False, weights='imagenet')
# Freeze the base model
base_model.trainable = False

# Add Custom layers
out_layer = tf.keras.layers.Conv2D(128, (1, 1), padding='SAME', activation=None)(base_model.output)
out_layer = tf.keras.layers.BatchNormalization()(out_layer)
out_layer = tf.keras.layers.ReLU()(out_layer) # 7x7x128

out_layer = tf.keras.layers.GlobalAveragePooling2D()(out_layer) # 128

out_layer = tf.keras.layers.Dense(2, activation='softmax')(out_layer)

# Make New Model
model = tf.keras.models.Model(base_model.input, out_layer)

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              metrics=['accuracy'])

# Training
history = model.fit(train_generator, epochs=25,
                    validation_data=validation_generator, verbose=1)

# Save the trained model
model.save("saved_model.h5")