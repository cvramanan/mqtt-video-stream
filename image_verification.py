from math import dist
import cv2
import numpy as np

sourceImage = cv2.imread("./tip.jpg")
distImage = cv2.imread("./test.png")

print(sourceImage.all() == distImage.all())