import numpy as np
import cv2
from calibrate import undistort_image
from Thresholding import forward
from perspective import perspective_transform, inv_perspective_transform
from Lane import Lane
from fit_draw import fit_and_draw_lane
from measure_center_curvature import measure_center_curvature
from debug_mode import debug_mode
from write_text import write_text

gleft_fit = gright_fit = None
first_run = True


def pipeline(image, debug_mode_on):
    global gleft_fit, gright_fit, first_run
    l = Lane()
    undistorted_image = undistort_image(image)                          # correct camera distortion
    out_img = np.copy(undistorted_image)                                # Copy undistorted image to add it to the lanes at the end
    warped_image = perspective_transform(undistorted_image)             # Apply perspective transform on the undistorted_image
    thresholded_image = forward(warped_image)                                # Threshold the image
    leftx, lefty, rightx, righty = l.find_lanes(thresholded_image)           # Find the lane points
    # Fit a polynomial to the lane points and draw it
    left_fit, right_fit, lanes_image = fit_and_draw_lane(leftx, lefty, rightx, righty, gleft_fit, gright_fit, thresholded_image, first_run)
    gleft_fit = left_fit
    gright_fit = right_fit
    first_run = False
    # Get the original perspective of the color_lanes
    inv_lanes_image = inv_perspective_transform(lanes_image)
    # Add the lane-line image to the original image
    final_image = cv2.addWeighted(out_img, 1, inv_lanes_image, 0.6, 0)
    if debug_mode_on == "1":
        final_image = debug_mode(final_image, warped_image, thresholded_image, inv_lanes_image)
    offset, direction, curvature = measure_center_curvature(left_fit, right_fit, image.shape)
    output_image = write_text(final_image, offset, direction, curvature)
    return output_image
