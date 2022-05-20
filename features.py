import numpy as np
import cv2

# Change color-space of image before getting feature vector
def change_color_space(image, colour_space):
    # YUV: color encoding system Y is "luma" or brightness, U and V are Blue minus luma and Red minus luma
    if colour_space == 'YUV':
        img = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
    # YCrCb: used in digital systems similar to YUV, are used interchangeably with subtle difference in the way they are encoded
    elif colour_space == 'YCrCb':
        img = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
    else:
        img = image
    return img

# Get spatial features "raw pixels" through resizing image, convert each channel to column vector then stack the 3 channels
def get_spatial_features(image, size = (32, 32)):
    channel_1 = cv2.resize(image[: ,:, 0], size).ravel()            # For size (32, 32), it produces (1024, ) vector
    channel_2 = cv2.resize(image[:, :, 1], size).ravel()
    channel_3 = cv2.resize(image[:, :, 2], size).ravel()
    features = np.hstack((channel_1, channel_2, channel_3))         # For size (32, 32), it produces (3072, ) vector
    return features

# Get color features using histogram of each channel and concatenating them
def get_colour_features(image, bins = 32):                          # bins is the number of discrete values in the histogram
    channel_1 = np.histogram(image[:, :, 0], bins=bins)
    channel_2 = np.histogram(image[:, :, 1], bins=bins)
    channel_3 = np.histogram(image[:, :, 2], bins=bins)
    features = np.concatenate((channel_1[0], channel_2[0], channel_3[0]))
    return features

# Get HOG features and turn it to column vector
def get_hog_features(image):
    # windowSize, blockSize,blockStride,cellSize,nbins
    # windowSize: the size of window sliding over the image
    # blockSize: a block contain multiple cells, we normalize gradient over blocks (size is in pixels)
    # cellSize: a histogram is created for each cell then it is normalized over the block (size is in pixels)
    # blockStride: as cell size
    # nbins: the number of discrete orientations
    features = cv2.HOGDescriptor((64, 64), (16, 16), (8, 8), (8, 8), 9).compute(image)
    features = np.ravel(features)                                   # generate a column vector
    return features