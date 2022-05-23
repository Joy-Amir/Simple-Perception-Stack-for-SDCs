import numpy as np
import cv2
from features import change_color_space, get_spatial_features, get_colour_features, get_hog_features


def get_features(image, colour_space='YUV', size=(64, 64), type='All'):                # feature type is All or HOG
    if size != (64, 64):                                        # resize image to get features
        image = cv2.resize(image, (64, 64))
    image = change_color_space(image, colour_space)             # change colour_space of the image
    if type == 'All':
        image_features = []
        image_features.append(get_spatial_features(image))
        image_features.append(get_colour_features(image))
        image_features.append(get_hog_features(image))
        features = np.concatenate(image_features)
    else:
        features = get_hog_features(image)
    return features
