import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import exposure

def debug_mode(output_img, mask):
    # binary images should be converted to colored maybe using dstack

    # img_cdf, bin_centers = exposure.cumulative_distribution(heatmap_pre)
    # heatmap_pre = np.interp(heatmap_pre, bin_centers, img_cdf)
    # print(heatmap_pre.shape, heatmap_pre.dtype)

    scale_percent = 25

    # calculate the percent of original dimensions
    width = int(output_img.shape[1] * scale_percent / 100)
    height = int(output_img.shape[0] * scale_percent / 100)
    dsize = (width, height)

    # resizing the 2 images with the same size
    # heatmap_pre_output = cv2.resize(heatmap_pre, dsize)
    mask_output = cv2.resize(mask, dsize)

    # putting the images in foreground, background
    # foreground1, foreground2, background = heatmap_pre_output, mask_output, output_img.copy()
    foreground1, background = mask_output, output_img.copy()

    # blending the images
    alpha = 1
    blended_portion1 = cv2.addWeighted(foreground1, alpha,
                                       background[200:200 + height, 10:10 + width, :],
                                       1-alpha,
                                       0,
                                       background, dtype=cv2.CV_64F)
    background[200:200 + height, 10:10 + width, :] = blended_portion1
    # blended_portion2 = cv2.addWeighted(foreground2, alpha,
    #                                    background[220 + height:220 + 2*height, 10:10 + width, :],
    #                                    1 - alpha,
    #                                    0,
    #                                    background, dtype=cv2.CV_64F)
    # background[220 + height:220 + 2*height, 10:10 + width, :] = blended_portion2
    return background


