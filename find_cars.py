import cv2
from prediction import get_features
import joblib


mlp = joblib.load('models/MLP, YUV, ALL/mlp_model.pkl')  # loading the multilayer perceptron model
X_scaler = joblib.load('models/MLP, YUV, ALL/scaler.pkl')  # loading a transform for images normalization as in training


def slide_window(img, x_start_stop=[None, None], y_start_stop=[None, None],
                    xy_window=(64, 64), xy_overlap=(0.75, 0.75)):
    # setting default values for the part of the image to be rendered to be the whole image
    if x_start_stop[0] is None:
        x_start_stop[0] = 0
    if x_start_stop[1] is None:
        x_start_stop[1] = img.shape[1]
    if y_start_stop[0] is None:
        y_start_stop[0] = 0
    if y_start_stop[1] is None:
        y_start_stop[1] = img.shape[0]

    # determining the axes range
    xspan = x_start_stop[1] - x_start_stop[0]
    yspan = y_start_stop[1] - y_start_stop[0]

    # determining the step of the window to be slided (in pixels)
    nx_pix_per_step = int(xy_window[0]*(1 - xy_overlap[0]))  # moving 0.25 of the window pixels to ensure overlap
    ny_pix_per_step = int(xy_window[1]*(1 - xy_overlap[1]))

    # calculating the number of windows to cover each axes with the step we decided
    nx_windows = int(xspan/nx_pix_per_step)
    ny_windows = int(yspan/ny_pix_per_step)

    # creating window list and passing on it vertically and horizontally
    # creating a window using the vertices of it in shape ((startx, starty), (endx , endy))
    # as if they are the 2 vertices on a diagonal from top to bottom from left to right
    window_list = []
    for ys in range(ny_windows):
        for xs in range(nx_windows):
            startx = xs * nx_pix_per_step + x_start_stop[0]
            endx = (xs+1) * nx_pix_per_step + x_start_stop[0]
            starty = ys * ny_pix_per_step + y_start_stop[0]
            endy = (ys+1) * ny_pix_per_step + y_start_stop[0]
            window_list.append(((startx, starty), (endx, endy)))
    return window_list


def find_cars(image):

    # creating a list for the windows that have a vehicle detected
    on_windows = []

    # Parameters
    # parameters for passing different window sizes
    pxs = 384 #448 #320
    INCREMENT_SIZE_BY = 16
    PXS_LIMIT = 720
    y_start_stop = [400, 660]  # to search for cars in the lower part of the image #[400, 660]
    xy_overlap = (0.8, 0.8)  # overlap between the windows #(0.8, 0.8)

    ACCEPTANCE_THRESHOLD = .99  # to accept the probability of detected cars more than this probability

    while pxs < PXS_LIMIT:
        windows = slide_window(image, x_start_stop=[700, None], y_start_stop=y_start_stop, xy_window=(pxs, pxs), xy_overlap=xy_overlap)
        for window in windows:
            # resizing the window to fit like the rest of the training images
            resized = cv2.resize((image[window[0][1]: window[1][1], window[0][0]: window[1][0]]), (64, 64))
            features = get_features(resized).reshape(1, -1)  # reshaping it to get one sample/img unlike in the training

            # applying normalization on the extracted features
            x_scaled = X_scaler.transform(features)

            if resized.shape[0] > 0:
                # check if the model predicts there is car in the window greater than the ACCEPTANCE_THRESHOLD
                if mlp.predict_proba(x_scaled.reshape(1, -1))[0][1] > ACCEPTANCE_THRESHOLD:
                    on_windows.append(window)
        pxs += INCREMENT_SIZE_BY

    return on_windows
