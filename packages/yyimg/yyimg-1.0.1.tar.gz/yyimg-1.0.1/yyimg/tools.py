#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : tools.py
#   Author      : YunYang1994
#   Created date: 2019-11-25 20:21:03
#   Description :
#
#================================================================


import cv2
import colorsys
import numpy as np
import imageio

def draw_2Dbox(image, bboxes, class_category):
    """
    image : numpy.ndarray
    bboxes: [cls_id, x_min, y_min, x_max, y_max] format coordinates.
    classes: ["person", "bus", ... ]
    """
    num_classes = len(class_category)
    fontScale = 0.5
    image_h, image_w, _ = image.shape
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]

    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

    for i, bbox in enumerate(bboxes):
        coor = np.array(bbox[1:5], dtype=np.int32)
        cls_id = int(bbox[0])
        bbox_color = colors[cls_id]
        c1, c2 = (coor[0], coor[1]), (coor[2], coor[3])
        cv2.rectangle(image, c1, c2, bbox_color, 2)

        bbox_mess = '%s' % class_category[cls_id]
        t_size = cv2.getTextSize(bbox_mess, 0, fontScale, thickness=1)[0]
        cv2.rectangle(image, c1, (c1[0] + t_size[0], c1[1] - t_size[1] - 3),
                      bbox_color, -1)  # filled
        cv2.putText(image, bbox_mess, (c1[0], c1[1]-2), cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale, (0, 0, 0), 1, lineType=cv2.LINE_AA)
    return image

def create_gif(gif_name, frames, duration=0.5):
    '''
    creat GIF
    '''
    new_frames = []
    for image in frames:
        frames.append(imageio.imread(image))
    imageio.mimsave(gif_name, new_frames, 'GIF', duration = duration)
    return





