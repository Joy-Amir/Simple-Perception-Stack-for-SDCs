import numpy as np
import cv2
import joblib                                                               # Used in saving and loading the model and normalizer
import glob                                                                 # Used in reading training images from a folder
from sklearn.preprocessing import StandardScaler                            # Used in normalizing the feature vector
from skimage.io import imread                                               # Used in loading image in RGB color space
from sklearn.neural_network import MLPClassifier                            # Used in training a multi-layer perceptron classifier
from sklearn.svm import LinearSVC                                           # Used in training Support vector machine classifier
from sklearn.model_selection import train_test_split                        # Used in splitting images to training and testing sets
from features import change_color_space, get_spatial_features, get_colour_features, get_hog_features

def get_train_features(images, colour_space='YUV', size=(64, 64), type = 'All'):                # feature type is All or HOG
    features = []                                                   # list of all training images features
    for filename in images:
        image = imread(filename)                                    # read image in RGB format
        if size != (64, 64):                                        # resize image to get features
            image = cv2.resize(image, size)
        image = change_color_space(image, colour_space)             # change colour_space of the image
        if type == 'All':
            image_features = []
            image_features.append(get_spatial_features(image))
            image_features.append(get_colour_features(image))
            image_features.append(get_hog_features(image))
            features.append(np.concatenate(image_features))
        else:
            features.append(get_hog_features(image))
    return features

# Normalize the features for faster training
def normalize_features(vehicle_features, non_vehicle_features):
    if (len(vehicle_features[0] > 0)):
        # stach features vertically, each example in a row
        X = np.vstack((vehicle_features, non_vehicle_features)).astype(np.float64)
        # StandardScaler: remove mean and scaling to unit variance
        # fit: Compute the mean and std to be used for later scaling.
        X_scaler = StandardScaler().fit(X)                          # Define a normalizer
        scaled_X = X_scaler.transform(X)                            # Perform standardization by centering and scaling
    return scaled_X, X_scaler

def train(colour_space, type, classifier):                          # classifier: MLP or SVC, feature type is All or HOG
    # Read the vehicle and non-vehicle images
    vehicles = glob.glob('Data/vehicles/*/*.png')
    non_vehicles = glob.glob('Data/non-vehicles/*/*.png')
    # Get the images features
    vehicle_features = get_train_features(vehicles, colour_space=colour_space, type=type)
    non_vehicle_features = get_train_features(non_vehicles, colour_space=colour_space, type=type)
    # Normalize the features
    scaled_X, X_scaler = normalize_features(vehicle_features, non_vehicle_features)
    # Form the output vector: 1 ---> vehicle, 0 ---> non_vehicle
    labels = np.hstack((np.ones(len(vehicle_features)), np.zeros(len(non_vehicle_features))))
    # test_size: ratio of test images to total images
    X_train, X_test, y_train, y_test = train_test_split(scaled_X, labels, test_size=0.2, random_state=4000)
    if (classifier == 'MLP'):
        mlp = MLPClassifier(random_state=999)                       # define mlp classifier
        mlp.fit(X_train, y_train)                                   # fit the training data
        joblib.dump(mlp, 'mlp_model.pkl')                           # save the model
        # Print training set and testing set accuracy
        print('MLP results')
        print('accuracy on training data: ', mlp.score(X_train, y_train))
        print('accuracy on test data: ', mlp.score(X_test, y_test))
    else:
        svc = LinearSVC()                                           # define SVC classifier
        svc.fit(X_train, y_train)                                   # fit the training data
        joblib.dump(svc, 'svc_model.pkl')                           # save the model
        # Print training set and testing set accuracy
        print('SVC results')
        print('accuracy on training data: ', svc.score(X_train, y_train))
        print('accuracy on test data: ', svc.score(X_test, y_test))

    joblib.dump(X_scaler, 'scaler.pkl')
    return

# classifier: feature type is All or HOG, MLP or SVC, YUV or YCrCb
train('YUV','All', 'SVC')




