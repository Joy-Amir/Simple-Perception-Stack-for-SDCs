# Define the dimensions of checkerboard
import cv2
import numpy as np
import glob
import pickle

# https://opencv24-python-tutorials.readthedocs.io/en/stable/py_tutorials/py_calib3d/py_calibration/py_calibration.html
# This function is used to obtain the camera matrix, distortion coefficients, rotation and translation vectors.
# These will be used to correct the error in photos resulting from the camera lens.
# eg: straight lines appear curvy, specially away from the origin.
def calibrate():

    # We need to get 3D object points representing real coordinates and their corresponding 2D points representing
    # the camera coordinates.
    # We will use chessboard images for this sake as in reality, the corners are equally distant so we can get the
    # real coordinates easily by creating array [0. 0. 0.], [1. 0. 0.], [2. 0. 0.].....[8, 5, 0].
    # Note: the z-axis values are assumed to be 0.
    objp = np.zeros((9 * 6, 3), np.float32)

    # np.mgrid function help in creating a numpy array of grid coordinates as stated above
    # The last column is left = 0 "for the z-axis"
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)


    # List for all object points & img points from all images
    objpoints = []
    imgpoints = []

    # Directory for all chessboard images used in calibration
    images = glob.glob('camera_cal/calibration2.jpg')
    for img in images:
        image = cv2.imread(img)                                            # Read the images
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)               # Convert to GRAY for the findChessboardCorners fn
        # Get 9x6 corners coordinates of chessboard. return_val = TRUE if corners are found
        return_val, corners = cv2.findChessboardCorners(gray_image, (9, 6), None)

        # If the corners are found, append the objp to object points and the corresponding corners to imgpoints
        if return_val == True:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Uncomment these lines to see the detected corners
            #img = cv2.drawChessboardCorners(image, (9, 6), corners, return_val)
            #cv2.imshow('img', img)
            #cv2.waitKey(50000)

    # Get the image size: (horizontal, vertical)
    image_size =(image.shape[1], image.shape[0])

    # Get the camera matrix, distortion coefficients, rotation and translation vectors
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, image_size, None, None)
    param = {}
    param['mtx'] = mtx
    param['dist'] = dist
    pickle.dump(param, open('calibration_param.pickle', 'wb'))


# Use the camera matrix, distortion coefficients to undistort the image
def undistort_image(image):
    # Read saved parameters
    with open('calibration_param.pickle', mode='rb') as f:
        param = pickle.load(f)
    mtx = param['mtx']
    dist = param['dist']
    undistorted_image = cv2.undistort(image, mtx, dist, None, mtx)
    return undistorted_image



# Testing
#calibrate()
#image = cv2.imread('road2.jpg')
#undistorted_image = undistort_image(image)
#undistorted_image_RGB = cv2.cvtColor(undistorted_image, cv2.COLOR_BGR2RGB)
#plt.imshow(undistorted_image_RGB)
#plt.show()

