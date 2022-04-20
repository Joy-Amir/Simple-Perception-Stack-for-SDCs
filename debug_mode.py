import numpy as np
import cv2


def debug_mode(output_img, perspective_transform_img, threshold_img, color_lanes_img):
    # binary images should be converted to colored maybe using dstack
    threshold_img = np.dstack((threshold_img, threshold_img, threshold_img))

    # percent by which the image is resized
    scale_percent = 25

    # calculate the 50 percent of original dimensions
    width = int(output_img.shape[1] * scale_percent / 100)
    height = int(output_img.shape[0] * scale_percent / 100)
    dsize = (width, height)

    # resizing the 3 images with the same size
    perspective_transform_output = cv2.resize(perspective_transform_img, dsize)
    threshold_output = cv2.resize(threshold_img, dsize)
    color_lanes_output = cv2.resize(color_lanes_img, dsize)

    # putting the images in foreground, background
    foreground1, foreground2, foreground3, background = perspective_transform_output, threshold_output,  \
                                                                    color_lanes_output, output_img.copy()

    # blending the images
    alpha = 1
    blended_portion1 = cv2.addWeighted(foreground1, alpha,
                                       background[40:40 + height, background.shape[1] - width - 10:background.shape[1] - 10, :],
                                       1-alpha,
                                       0,
                                       background)
    background[40:40 + height, background.shape[1] - width - 10:background.shape[1] - 10, :] = blended_portion1
    blended_portion2 = cv2.addWeighted(foreground2, alpha,
                                       background[60+height:60 + 2*height, background.shape[1] - width - 10:background.shape[1] - 10, :],
                                       1 - alpha,
                                       0,
                                       background)
    background[60+height:60 + 2*height, background.shape[1] - width - 10:background.shape[1] - 10, :] = blended_portion2
    blended_portion3 = cv2.addWeighted(foreground3, alpha,
                                       background[80 + 2*height:80 + 3*height, background.shape[1] - width - 10:background.shape[1] - 10, :],
                                       1 - alpha,
                                       0,
                                       background)
    background[80 + 2*height:80 + 3*height, background.shape[1] - width - 10:background.shape[1] - 10, :] = blended_portion3
    return background


