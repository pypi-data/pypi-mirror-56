from .version import __version__
from .tools import draw_2Dbox, create_gif
from .utils import read_text
from .augments import random_translate, random_crop, horizontal_flip, shift_gamma, shift_brightness, shift_color
from .augments import add_rain


def load_data():
    """
    Return:
        @image, a numpy array of shape (N, height, width, #channels)
        @boxes, a numpy array of shape (N, 5), representing N boxes
                "class_index, xmin, ymin, xmax, ymax"
        @classes, a list of class names
    """
    import os
    import cv2
    import numpy as np
    dirpath = os.path.dirname(os.path.abspath(__file__))
    image = cv2.imread(os.path.join(dirpath, "000998.png.py"))
    boxes = np.array([
        [  0.     , 582.99   , 180.48999, 615.14   , 211.09   ],
        [  3.     , 850.75   , 163.71   , 892.42   , 270.95   ],
        [  0.     , 696.89   , 182.62   , 826.96   , 273.94   ],
        [  0.     , 668.45996, 180.61   , 742.13995, 244.07   ],
        [  0.     , 642.69   , 175.2    , 679.51   , 210.86   ],
        [  0.     , 172.57999, 200.24   , 325.09998, 276.74   ],
        [  0.     , 282.46997, 189.66   , 387.62997, 249.08   ],
        [  0.     , 372.78   , 186.11   , 441.8    , 227.82   ],
        [  0.     , 631.13   , 176.96   , 651.28   , 196.17001]],)
    classes = ['Car', 'Truck', 'Van', 'Pedestrian']
    return image, boxes, classes


__all__ = [draw_2Dbox, read_text, load_data]
