#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : augmets.py
#   Author      : YunYang1994
#   Created date: 2019-11-17 11:06:12
#   Description :
#
#================================================================

import cv2
import random
import numpy as np

def random_translate(image, bboxes, seed=1):
    random.seed(seed)
    h, w, _ = image.shape
    max_bbox = np.concatenate([np.min(bboxes[:, 1:3], axis=0), np.max(bboxes[:, 3:5], axis=0)], axis=-1)

    max_l_trans = max_bbox[0]
    max_u_trans = max_bbox[1]
    max_r_trans = w - max_bbox[2]
    max_d_trans = h - max_bbox[3]

    tx = random.uniform(-(max_l_trans - 1), (max_r_trans - 1))
    ty = random.uniform(-(max_u_trans - 1), (max_d_trans - 1))

    M = np.array([[1, 0, tx], [0, 1, ty]])
    image = cv2.warpAffine(image, M, (w, h))

    bboxes[:, [1, 3]] = bboxes[:, [1, 3]] + tx
    bboxes[:, [2, 4]] = bboxes[:, [2, 4]] + ty
    return image, bboxes

def random_crop(image, bboxes, seed=1):
    random.seed(seed)
    h, w, _ = image.shape
    max_bbox = np.concatenate([np.min(bboxes[:, 1:3], axis=0), np.max(bboxes[:, 3:5], axis=0)], axis=-1)

    max_l_trans = max_bbox[0]
    max_u_trans = max_bbox[1]
    max_r_trans = w - max_bbox[2]
    max_d_trans = h - max_bbox[3]

    crop_xmin = max(0, int(max_bbox[0] - random.uniform(0, max_l_trans)))
    crop_ymin = max(0, int(max_bbox[1] - random.uniform(0, max_u_trans)))
    crop_xmax = max(w, int(max_bbox[2] + random.uniform(0, max_r_trans)))
    crop_ymax = max(h, int(max_bbox[3] + random.uniform(0, max_d_trans)))

    image = image[crop_ymin : crop_ymax, crop_xmin : crop_xmax]

    bboxes[:, [1, 3]] = bboxes[:, [1, 3]] - crop_xmin
    bboxes[:, [2, 4]] = bboxes[:, [2, 4]] - crop_ymin

    return image, bboxes


def horizontal_flip(image, bboxes, seed=1):
    random.seed(seed)
    _, w, _ = image.shape
    flip_image = image[:, ::-1, :].copy()
    bboxes[:, [1,3]] = w - bboxes[:, [3,1]]

    return flip_image, bboxes

def shift_gamma(image, seed=1):
    random.seed(seed)
    # randomly shift gamma
    gamma = random.uniform(0.8, 1.2)
    print(gamma)
    image = image.copy() ** gamma
    image = np.clip(image, 0, 255)
    return image.astype(np.uint8)

def shift_brightness(image, seed=None):
    random.seed(seed)
    # randomly shift brightness
    brightness = random.uniform(0.5, 2.0)
    image = image.copy() * brightness
    image = np.clip(image, 0, 255)
    return image.astype(np.uint8)

def shift_color(image, seed=None):
    random.seed(seed)
    # randomly shift color
    colors = [random.uniform(0.8, 1.2) for _ in range(3)]
    white = np.ones([image.shape[0], image.shape[1]])
    color_image = np.stack([white * colors[i] for i in range(3)], axis=2)
    image = image.copy().astype(np.float32) * color_image.astype(np.float32)
    image = np.clip(image, 0, 255)
    return image.astype(np.uint8)

def get_noise(image, value, seed=None):
    noise = np.random.uniform(0,256,image.shape[0:2])
    noise[np.where(noise<(256-value))]=0

    k = np.array([ [0, 0.1, 0], [0.1,  8, 0.1], [0, 0.1, 0] ])

    noise = cv2.filter2D(noise,-1,k)
    return noise

def rain_blur(noise, length=10, angle=0, w=1):
    trans = cv2.getRotationMatrix2D((length/2, length/2), angle-45, 1-length/100.0)
    dig = np.diag(np.ones(length))
    k = cv2.warpAffine(dig, trans, (length, length))
    k = cv2.GaussianBlur(k,(w,w),0)
    blurred = cv2.filter2D(noise, -1, k)
    cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
    blurred = np.array(blurred, dtype=np.uint8)
    return blurred

def add_rain(img, beta = 0.8):
    noise = get_noise(img, value=1)
    rain = rain_blur(noise,length=20,angle=-30,w=3)
    rain = np.expand_dims(rain,2)
    rain_effect = np.concatenate((img,rain),axis=2)  #add alpha channel

    rain_result = img.copy()
    rain = np.array(rain,dtype=np.float32)
    rain_result[:,:,0] = rain_result[:,:,0] * (255-rain[:,:,0])/255 + beta*rain[:,:,0]
    rain_result[:,:,1] = rain_result[:,:,1] * (255-rain[:,:,0])/255 + beta*rain[:,:,0]
    rain_result[:,:,2] = rain_result[:,:,2] * (255-rain[:,:,0])/255 + beta*rain[:,:,0]
    return rain_result
