import tensorflow as tf

import os
import pathlib
import time
import datetime
import numpy as np
from matplotlib import pyplot as plt
import cv2
from tensorflow.keras.models import Sequential, model_from_json


# model 
model_h5 = "E:\\GitHub\\Covid_GAN\\ModelPix2Pix\\genrator.h5"
model_json = "E:\\GitHub\\Covid_GAN\\ModelPix2Pix\\genrator.json"

def generate_images(model, test_input, tar):
  prediction = model(test_input, training=True)
  plt.figure(figsize=(15, 15))

  display_list = [test_input[0,:,:,:], tar[0,:,:,:], prediction[0,:,:,:]]
  title = ['Input Image', 'Ground Truth', 'Predicted Image']
  
  for i in range(3):
    plt.subplot(1, 3, i+1)
    plt.title(title[i])
    # Getting the pixel values in the [0, 1] range to plot.
    print(i)
    plt.imshow(display_list[i] * 0.5 + 0.5)
    plt.axis('off')
  plt.show()

with open(model_json, 'r') as f:
  loaded_model = model_from_json(f.read())
   
loaded_model.load_weights(model_h5)

test = "E:\\GitHub\\Covid_GAN\\DataSetInpainting_512\\train\\520.jpg"
IMG_WIDTH = 512
IMG_HEIGHT = 512

def resize(input_image, real_image, height, width):
  input_image = tf.image.resize(input_image, [height, width],
                                method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
  real_image = tf.image.resize(real_image, [height, width],
                               method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)

  return input_image, real_image



# Normalizing the images to [-1, 1]
def normalize(input_image, real_image):
  input_image = (input_image / 127.5) - 1
  real_image = (real_image / 127.5) - 1

  return input_image, real_image

def load(image_file):
  # Read and decode an image file to a uint8 tensor
  image = tf.io.read_file(image_file)
  image = tf.io.decode_jpeg(image)
  # Split each image tensor into two tensors:
  # - one with a real building facade image
  # - one with an architecture label image 
  w = tf.shape(image)[1]
  w = w // 2
#   input_image
  input_image = image[:, w:, :]
  real_image = image[:, :w, :]

  # Convert both images to float32 tensors
  input_image = tf.cast(input_image, tf.float32)
  real_image = tf.cast(real_image, tf.float32)

  return input_image, real_image

def load_image(image_file):
  input_image, real_image = load(image_file)
  input_image, real_image = resize(input_image, real_image,
                                   IMG_HEIGHT, IMG_WIDTH)
  input_image, real_image = normalize(input_image, real_image)

  return input_image, real_image

inp, re  = load_image(test)
inp = np.expand_dims(inp, axis=0)
re = np.expand_dims(re, axis=0)
generate_images(loaded_model,inp, re)