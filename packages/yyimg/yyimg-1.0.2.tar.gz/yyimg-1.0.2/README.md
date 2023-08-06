<p align="center">
    <img width="65%" src="https://user-images.githubusercontent.com/30433053/68877902-c5bd2f00-0741-11ea-8cac-af227a77bb14.png" style="max-width:65%;">
    </a>
</p>

# Introduction
yyimg is a high-level image-processing tool, written in Python and using [OpenCV](https://github.com/opencv/opencv) as backbend. This repo helps you with processing images for your deep learning projects. 

# Installation
Commands to install from pip or download the source code from our website https://pypi.org/project/yyimg

```bashrc
$ pip3 install yyimg==1.0.0rc
```

# Example Useage

Take one image in Kitti dataset for example:

```python
import yyimg
from PIL import Image
image, boxes, classes = yyimg.load_data()
```
|Items|Description|
|---|---
|image|a numpy array of shape (height, width, #channels)
|boxes|a numpy array of shape (N, 5), representing N 2Dboxes of `[class_index, xmin, ymin, xmax, ymax]`
|classes|a list of class names

```python
print(classes)
['Car', 'Truck', 'Van', 'Pedestrian']
```

## visualize 2D boxes

```python
draw_image = yyimg.draw_2Dbox(image, boxes, class_category=classes)
draw_image = cv2.cvtColor(draw_image, cv2.COLOR_BGR2RGB) # BGR -> RGB
Image.fromarray(draw_image).show()
```
![image](https://user-images.githubusercontent.com/30433053/69005372-49526800-095c-11ea-8984-4d03154eab80.jpg)

## data augmentation

### - horizontal_flip

with 2D bounding boxes:
```python
aug_image, boxes = yyimg.horizontal_flip(image, boxes)
```
without 2D bounding boxes:
```python
aug_image = yyimg.horizontal_flip(image)
```
![image](https://user-images.githubusercontent.com/30433053/69005858-b668fc00-0962-11ea-89a9-2e06bf14fb2d.jpg)

### - add_rain

```python
aug_image = yyimg.add_rain(image)
```
![image](https://user-images.githubusercontent.com/30433053/69005561-d0084480-095e-11ea-9b8d-c94f7694585b.jpg)

### - shift_gama

```python
aug_image = yyimg.shift_gamma(image) 
```
![image](https://user-images.githubusercontent.com/30433053/69005465-c7633e80-095d-11ea-856c-9bc22b213e5c.jpg)

### - shift_brightness

```python
aug_image = yyimg.shift_brightness(image)
```
![image](https://user-images.githubusercontent.com/30433053/69005494-435d8680-095e-11ea-9922-1ee73571b645.jpg)

### - shift_color

```python
aug_image = yyimg.shift_color(image)
```
![image](https://user-images.githubusercontent.com/30433053/69005754-6f2e3b80-0961-11ea-9095-ed5c0497dcdc.jpg)


