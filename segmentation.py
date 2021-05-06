## @package Segmentation_app
# Segmentation code of Tensorflow Keras model
# 
#  @version 1 
#
# Pontificia Universidad Javeriana
# 
# Electronic Enginnering
# 
# Developed by:
# - Andrea Juliana Ruiz Gomez
#       Mail: <andrea_ruiz@javeriana.edu.co>
#       GitHub: andrearuizg
# - Pedro Eli Ruiz Zarate
#       Mail: <pedro.ruiz@javeriana.edu.co>
#       GitHub: PedroRuizCode
#  
# With support of:
# - Francisco Carlos Calderon Bocanegra
#       Mail: <calderonf@javeriana.edu.co>
#       GitHub: calderonf
# - John Alberto Betancout Gonzalez
#       Mail: <john@kiwibot.com>
#       GitHub: JohnBetaCode


import os
import numpy as np
import cv2
from glob import glob
from time import time
import tensorflow as tf
from tensorflow.keras import models
from tqdm import tqdm


images = glob(os.path.join("media/", "test/*"))
model = models.load_model("files/model.h5")


if __name__ == "__main__":
    result1 = np.zeros((360, 640, 3), np.uint8)
    result2 = np.zeros((360, 640, 3), np.uint8)
    for i in tqdm(range(len(images))):
        if (images[i].split('.')[-1]) == "mp4":
            vid = cv2.VideoCapture(images[i])
            fourcc = cv2.VideoWriter_fourcc(*'MP4V')
            str_file = (images[i].split('/')[-1]).split('.')[0]
            filename = "results/color/%s.mp4" % (str_file)
            filename1 = "results/mask%s-mask-predicted.mp4" % (str_file)
            out1 = cv2.VideoWriter(filename, fourcc, 30.0, (640, 360))
            out2 = cv2.VideoWriter(filename1, fourcc, 30.0, (640, 360))
            while(vid.isOpened()):
                ret, image1 = vid.read()
                if ret is True:
                    image2 = cv2.resize(image1, (256, 256))
                    image = image2 / 255.0
                    image = np.reshape(image, [256, 256, 3])
                    t1 = time()
                    result = model.predict(np.expand_dims(image, axis=0))[0] > 0.5
                    print(time() - t1)
                    result = result * 255.0
                    result = cv2.resize(result, (640, 360), interpolation=cv2.INTER_AREA)
                    result2 = cv2.resize(result, (640, 360), interpolation=cv2.INTER_AREA)
                    result2 = result2 / 255.0
                    result1 = cv2.cvtColor(result.astype('uint8'), cv2.COLOR_GRAY2BGR)
                    result1[..., 0] = np.where(result1[..., 0], 90, 0).astype('uint8')
                    result1[..., 1] = 0
                    result1 = cv2.addWeighted(image1, 0.7, result1, 0.3, 0)
                    out1.write(result1)
                    out2.write(cv2.cvtColor(result2.astype('uint8'), cv2.COLOR_GRAY2BGR))
                else:
                    break
            vid.release()
            out1.release()
            out2.release()
        else:
            image1 = cv2.imread(images[i], cv2.IMREAD_COLOR)
            image2 = cv2.resize(image1, (256, 256))
            image = image2 / 255.0
            image = np.reshape(image, [256, 256, 3])
            t1 = time()
            result = model.predict(np.expand_dims(image, axis=0))[0] > 0.5
            print(time() - t1)
            result = result * 255.0
            result = cv2.resize(result, (640, 360), interpolation=cv2.INTER_AREA)
            result2 = cv2.resize(result, (640, 360), interpolation=cv2.INTER_AREA)
            result2 = result2 / 255.0
            result1 = cv2.cvtColor(result.astype('uint8'), cv2.COLOR_GRAY2BGR)
            result1[..., 0] = np.where(result1[..., 0], 90, 0).astype('uint8')
            result1[..., 1] = 0
            result1 = cv2.addWeighted(image1, 0.7, result1, 0.3, 0)
            str_file = (images[i].split('/')[-1]).split('.')[0]
            filename = "results/color/%s-predicted.png" % (str_file)
            filename1 = "results/mask/%s-mask-predicted.png" % (str_file)
            cv2.imwrite(filename, result1)
            cv2.imwrite(filename1, result2)
