#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : utils.py
#   Author      : YunYang1994
#   Created date: 2019-11-14 16:17:30
#   Description :
#
#================================================================

import numpy as np

def read_text(path):
    bboxes = []
    lines = open(path).readlines()
    for line in lines:
        label = line.split()
        bboxes.append(label)
    return np.array(bboxes, dtype=np.float32)


