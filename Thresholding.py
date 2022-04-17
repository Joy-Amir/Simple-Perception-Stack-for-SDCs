import cv2
import numpy as np
import matplotlib.pyplot as plt


def threshold_rel(img, lo, hi):  # lo, hi is percentage of the intensities range i have
    vmin = np.min(img)  # get minimum pixels in an image
    vmax = np.max(img)  # get max pixels in the image

    vlo = vmin + (vmax - vmin) * lo  # interpolation on vlo, vhi to map 0.8->1 (lo->hi) to range of vmin->vmax
    vhi = vmin + (vmax - vmin) * hi
    return np.uint8((img >= vlo) & (
                img <= vhi)) * 255  # if img is within a certain range then the condition is true=1, 1*255= white pixels


def threshold_abs(img, lo, hi):
    return np.uint8((img >= lo) & (img <= hi)) * 255  # check if the img is within the range


def forward(img):
    """ Take an image and extract all relavant pixels.
    Parameters:
        img (np.array): Input image
    Returns:
        binary (np.array): A binary image represent all positions of relavant pixels.
    """
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # All these channels are for edge detection
    h_channel = hls[:, :, 0]
    l_channel = hls[:, :, 1]  # l_channel is used to check lightening for weather conditions of the video
    s_channel = hls[:, :, 2]
    v_channel = hsv[:, :, 2]

    right_lane = threshold_rel(l_channel, 0.8, 1.0)  # l_channel of white color range
    right_lane[:, :750] = 0  # why

    left_lane = threshold_abs(h_channel, 20, 30)  # hue lower and upper range of yellow color
    left_lane &= threshold_rel(v_channel, 0.7, 1.0)
    left_lane[:, 550:] = 0

    img2 = left_lane | right_lane

    return img2

image=cv2.imread("straight_lines2.jpg")
image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
im2=forward(image)
plt.imshow(im2)