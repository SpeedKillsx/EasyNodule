import numpy as np
from tqdm import tqdm
import tensorflow as tf
from datetime import datetime
from PIL import Image, ImageEnhance
import numpy as np
import pandas as pd
from PIL import ImageFilter
from matplotlib import pyplot as plt
import colorsys
import cv2 as cv
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from skimage.filters import gabor, gaussian

from pywt import dwt2
import pickle
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import tensorflow_io as tfio

import tensorflow_io as tfio
# Parameters Based on Paper
epsilon = 1e-7
m_plus = 0.8
m_minus = 0.5
lambda_ = 0.9
alpha = 0.001
epochs = 50
no_of_secondary_capsules = 2

optimizer = tf.keras.optimizers.Adam()

params = {
    "no_of_conv_kernels": 256,
    "no_of_primary_capsules": 32,
    "no_of_secondary_capsules": 2,
    "primary_capsule_vector": 32,
    "secondary_capsule_vector": 64,
    "r":5,
}
class CapsuleNetwork(tf.keras.Model):
    def __init__(self, no_of_conv_kernels, no_of_primary_capsules, primary_capsule_vector, no_of_secondary_capsules, secondary_capsule_vector, r):
        super(CapsuleNetwork, self).__init__()
        self.no_of_conv_kernels = no_of_conv_kernels
        self.no_of_primary_capsules = no_of_primary_capsules
        self.primary_capsule_vector = primary_capsule_vector
        self.no_of_secondary_capsules = no_of_secondary_capsules
        self.secondary_capsule_vector = secondary_capsule_vector
        self.r = r
        
        
        with tf.name_scope("Variables") as scope:
            self.convolution = tf.keras.layers.Conv2D(self.no_of_conv_kernels, [9,9], strides=[1,1], name='ConvolutionLayer', activation='relu')
            self.primary_capsule = tf.keras.layers.Conv2D(self.no_of_primary_capsules * self.primary_capsule_vector, [9,9], strides=[2,2], name="PrimaryCapsule", padding= "same")
            self.w = tf.Variable(tf.random_normal_initializer()(shape=[1, 4608, self.no_of_secondary_capsules, self.secondary_capsule_vector, self.primary_capsule_vector]), dtype=tf.float32, name="PoseEstimation", trainable=True)
            self.dense_1 = tf.keras.layers.Dense(units = 256, activation='relu')
            self.dropout_1 = tf.keras.layers.Dropout(0.5)
            self.dense_2 = tf.keras.layers.Dense(units = 512, activation='relu')
            self.dropout_2 = tf.keras.layers.Dropout(0.5)
            self.dense_3 = tf.keras.layers.Dense(units = 1024 , activation='sigmoid', dtype='float32')
            
    def build(self, input_shape):
        pass
        
    def squash(self, s):
        with tf.name_scope("SquashFunction") as scope:
            s_norm = tf.norm(s, axis=-1, keepdims=True)
            return tf.square(s_norm)/(1 + tf.square(s_norm)) * s/(s_norm + epsilon)
    
    
    def call(self, inputs):
        input_x, y = inputs
        
        x = self.convolution(input_x)
        x = self.primary_capsule(x) # x.shape: (None, 6, 6, 256) mais avec (64,64) , (None, 56,56,256)
    
        
        with tf.name_scope("CapsuleFormation") as scope:
            X_gabor = tfio.experimental.filter.gabor(x, freq=0.7 , theta=0.9 ).numpy()
            X_gabor = tf.cast(X_gabor, dtype="float32")
            
            u = tf.reshape(X_gabor, (-1, self.no_of_primary_capsules * x.shape[1] * x.shape[2], 32)) # u.shape: (None, 1152, 8)
            u = tf.expand_dims(u, axis=-2) # u.shape: (None, 1152, 1, 8)
            u = tf.expand_dims(u, axis=-1) # u.shape: (None, 1152, 1, 8, 1)
            u_hat = tf.matmul(self.w, u) # u_hat.shape: (None, 1152, 10, 16, 1)
            u_hat = tf.squeeze(u_hat, [4]) # u_hat.shape: (None, 1152, 10, 16)
            
        
        with tf.name_scope("DynamicRouting") as scope:
            
            b = tf.zeros((x.shape[0], 4608, self.no_of_secondary_capsules, 1)) # b.shape: (None, 1152, 10, 1)
         
            for i in range(self.r): # self.r = 3
                c = tf.nn.softmax(b, axis=-2) # c.shape: (None, 1152, 10, 1)
                s = tf.reduce_sum(tf.multiply(c, u_hat), axis=1, keepdims=True) # s.shape: (None, 1, 10, 16)
                v = self.squash(s) # v.shape: (None, 1, 10, 16)
                agreement = tf.squeeze(tf.matmul(tf.expand_dims(u_hat, axis=-1), tf.expand_dims(v, axis=-1), transpose_a=True), [4]) # agreement.shape: (None, 1152, 10, 1)
                
                b += agreement
                
        with tf.name_scope("Masking") as scope:
            y = tf.expand_dims(y, axis=-1) # y.shape: (None, 10, 1)
            y = tf.expand_dims(y, axis=1) # y.shape: (None, 1, 10, 1)
            mask = tf.cast(y, dtype=tf.float32) # mask.shape: (None, 1, 10, 1)
            v_masked = tf.multiply(mask, v) # v_masked.shape: (None, 1, 10, 16)
            
        with tf.name_scope("Reconstruction") as scope:
            v_ = tf.reshape(v_masked, [-1, self.no_of_secondary_capsules * self.secondary_capsule_vector]) # v_.shape: (None, 160)
            reconstructed_image = self.dense_1(v_) # reconstructed_image.shape: (None, 512)
            self.dropout_1
            reconstructed_image = self.dense_2(reconstructed_image) # reconstructed_image.shape: (None, 1024)
            self.dropout_2
            reconstructed_image = self.dense_3(reconstructed_image) # reconstructed_image.shape: (None, 784)
        
        return v, reconstructed_image

   
    def predict_capsule_output(self, inputs):
        
        x = self.convolution(inputs)
        x = self.primary_capsule(x) # x.shape: (None, 6, 6, 256)
        
        with tf.name_scope("CapsuleFormation") as scope:
            x_g = tfio.experimental.filter.gabor(x, freq=0.7 , theta=0.9 ).numpy()
            X_gabor = tf.cast(x_g, dtype="float32")
            u = tf.reshape(X_gabor, (-1, self.no_of_primary_capsules * x.shape[1] * x.shape[2], 32)) # u.shape: (None, 1152, 8)
            
            u = tf.expand_dims(u, axis=-2) # u.shape: (None, 1152, 1, 8)
            u = tf.expand_dims(u, axis=-1) # u.shape: (None, 1152, 1, 8, 1)
            u_hat = tf.matmul(self.w, u) # u_hat.shape: (None, 1152, 10, 16, 1)
            u_hat = tf.squeeze(u_hat, [4]) # u_hat.shape: (None, 1152, 10, 16)
            
        
        with tf.name_scope("DynamicRouting") as scope:
            b = tf.zeros((x.shape[0], 4608, self.no_of_secondary_capsules, 1)) # b.shape: (None, 1152, 10, 1)
            
            for i in range(self.r): # self.r = 3
                c = tf.nn.softmax(b, axis=-2) # c.shape: (None, 1152, 10, 1)
                s = tf.reduce_sum(tf.multiply(c, u_hat), axis=1, keepdims=True) # s.shape: (None, 1, 10, 16)
                v = self.squash(s) # v.shape: (None, 1, 10, 16)
                agreement = tf.squeeze(tf.matmul(tf.expand_dims(u_hat, axis=-1), tf.expand_dims(v, axis=-1), transpose_a=True), [4]) # agreement.shape: (None, 1152, 10, 1)
                
                b += agreement
        return v

    def regenerate_image(self, inputs):
       
        with tf.name_scope("Reconstruction") as scope:
            v_ = tf.reshape(inputs, [-1, self.no_of_secondary_capsules * self.secondary_capsule_vector]) # v_.shape: (None, 160)
            reconstructed_image = self.dense_1(v_) # reconstructed_image.shape: (None, 512)
            self.dropout_1
            reconstructed_image = self.dense_2(reconstructed_image) # reconstructed_image.shape: (None, 1024)
            self.dropout_2
            reconstructed_image = self.dense_3(reconstructed_image) # reconstructed_image.shape: (None, 784)
        return reconstructed_image

def Preprocessing(img):
    img = cv.resize(img, (64,64))
    #conversion vers Image
    #print("shape image ", img.shape)
    image = Image.fromarray(img)
    #print("image size : ", image.size)

    #Calcul des coordonnées pour couper le milieu de l'image
    width = 64 
    height = 64
    left = (width - 32) // 2
    top = (height - 32) // 2
    right = left + 32
    bottom = top + 32

    #Découpage de l'image
    sub_image = image.crop((left, top, right, bottom))

    #conversion vers numpy
    np_image = np.asarray(sub_image)
    #print("shape np image ", np_image.shape)
    np_image = cv.GaussianBlur(np_image, (3,3 ), 3)

    np_image = np_image / 255.0
    np_image = tf.cast(np_image, dtype=tf.float32)
    np_image = tf.expand_dims(np_image, axis=-1)
    return np_image


def safe_norm(v, axis=-1, epsilon=1e-7):
    v_ = tf.reduce_sum(tf.square(v), axis = axis, keepdims=True)
    return tf.sqrt(v_ + epsilon)

def predict(model, x):
    #print(type(x))
    #print(x.shape)
    pred = safe_norm(model.predict_capsule_output(x))
    pred = tf.squeeze(pred, [1])
    #print(pred)
    return np.argmax(pred, axis=1)[:,0]


def predictP(model, x):
    #print(type(x))
    pred = safe_norm(model.predict_capsule_output(x))
    pred = tf.squeeze(pred, [1])
    #print(pred)
    return pred


def predict_proba(model, x):
    #print(type(x))
    pred = safe_norm(model.predict_capsule_output(x))
    pred = tf.squeeze(pred, [1])
    return pred, np.argmax(pred, axis=1)[:,0]



def final_pred(imgX, imgY, imgZ, modelx, modely, modelz):
    imgX = Preprocessing(imgX)
    imgY = Preprocessing(imgY)
    imgZ = Preprocessing(imgZ)
    probaX, valX = predict_proba(modelx, tf.expand_dims(imgX, 0))
    probaY, valY = predict_proba(modely, tf.expand_dims(imgY, 0))
    probaZ, valZ = predict_proba(modelz, tf.expand_dims(imgZ, 0))
    somme = 0
    if (valX[0] == valY[0]) and (valY[0]== valZ[0]):
        return valX[0]
    else:
        #print("ici")
        somme  = (1.5* np.max(probaX)) + (1 * np.max(probaY)) + (2 * np.max(probaZ))
        #print(np.max(probaX))
        final_pred = somme / (1.5+1+2)
        #print(final_pred)
        #print(XM_trainY[i])
        #print(final_pred)
        if final_pred <=0.73:
            return 1
        else:
            return 0
        
    return valX[0]

def final_predMAJOR(imgX, imgY, imgZ, modelx, modely, modelz):
    
    imgX = Preprocessing(imgX)
    imgY = Preprocessing(imgY)
    imgZ = Preprocessing(imgZ)
    probaX, valX = predict_proba(modelx, tf.expand_dims(imgX, 0))
    probaY, valY = predict_proba(modely, tf.expand_dims(imgY, 0))
    probaZ, valZ = predict_proba(modelz, tf.expand_dims(imgZ, 0))
    somme = 0
    if (valX[0] == valY[0]) :
        #list_def_ref.append([i, imgX, imgY, None])
        return valX[0]
    else:
        if (valY[0]== valZ[0]):
            #list_def_ref.append([i, None,imgY, imgZ])
            return valY[0]
        else:
            if (valX[0]== valZ[0]):
                #list_def_ref.append([i, imgX,None, imgZ])
                return valX[0]
