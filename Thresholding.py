import cv2
import numpy as np
import matplotlib.pyplot as plt


def threshold_rel(img, lo, hi):
    vmin = np.min(img)  # get minimum pixels in an image
    vmax = np.max(img)  # get max pixels in the image

    # interpolation on vlo, vhi to map (lo->hi) to range of vmin->vmax
    vlo = vmin + (vmax - vmin) * lo
    vhi = vmin + (vmax - vmin) * hi
    return np.uint8((img >= vlo) & (img <= vhi)) * 255


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
    l_channel = hls[:, :, 1]  # l_channel is used to adjust lightening to cover different weather conditions
    s_channel = hls[:, :, 2]
    v_channel = hsv[:, :, 2]

    right_lane = threshold_rel(l_channel, 0.86, 1.0)  # l_channel of white color range
    right_lane[:, :750] = 0

    left_lane = threshold_abs(h_channel, 20,
                              30)  # hue lower and upper range of yellow or white color depending on the left lane color
    left_lane &= threshold_rel(v_channel, 0.7, 1.0)  # eliminate other objects than the straight line in the left lanes
    left_lane[:, 550:] = 0

    img2 = left_lane | right_lane

    return img2

# Test and run the function
# image=cv2.imread("straight_lines1.jpg")
# image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# im2=forward(image)
# plt.imshow(im2)

