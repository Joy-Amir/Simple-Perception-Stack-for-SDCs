import cv2
import numpy as np
import inv_perspective_transform


def draw_lane(warped_img, undistorted_img, left_fit_coef, right_fit_coef):
    """
    It takes the warped_img (bird eye's view) and the original image after undistortion.
    It takes the coefficients of the fit polynomial for the left and right lanes.
    It returns the undistorted image with the lane having a rectangle around it and highlighted.
    """

    # Generate y values then calculate x values from polynomial function
    plot_y = np.linspace(0, undistorted_img.shape[0]-1, undistorted_img.shape[0])
    plot_x_left = (left_fit_coef[0]*(plot_y**2)) + left_fit_coef[1]*plot_y + left_fit_coef[2]
    plot_x_right = (right_fit_coef[0]*(plot_y**2)) + right_fit_coef[1]*plot_y + right_fit_coef[2]

    # Create image to draw lines
    warp_zero = np.zeros_like(warped_img).astype(np.uint8)  # creating a black (zero values) gray-scale image
    warp_color = np.dstack((warp_zero, warp_zero, warp_zero))  # creating a black RGB image stack depth-wise

    # Arrange points in an array (x,y) in a polygon form
    pts_left_lane = np.array([np.transpose(np.vstack([plot_x_left, plot_y]))])  # pts starting from y=0
    pts_right_lane = np.array([np.flipud(np.transpose(np.vstack([plot_x_right, plot_y])))])  # pts starting from y = max
    pts = np.hstack((pts_left_lane, pts_right_lane))  # stacking them in a way to form a polygon anti-clockwise

    # Filling the shape with green color BGR
    cv2.fillPoly(warp_color, np.int_([pts]), (0, 255, 0))

    # Warp back the created image by inverse perspective function
    unwarped_poly = inv_perspective_transform(warp_color)

    # Add the created image on the undistorted image but with some translucency since the weight is a fraction
    result = cv2.addWeighted(undistorted_img, 1, unwarped_poly, 0.3, 0)

    # In the same way, create the two lines representing the lanes themselves
    lines_warp_color = np.dstack((warp_zero, warp_zero, warp_zero))

    cv2.polylines(lines_warp_color, np.int_([pts_left_lane]), isClosed=False, color=(0, 0, 255), thickness=25)  # Red
    cv2.polylines(lines_warp_color, np.int_([pts_right_lane]), isClosed=False, color=(255, 255, 0), thickness=25)  # B&G

    unwarped_lines = inv_perspective_transform(lines_warp_color)

    output_img = cv2.addWeighted(result, 1, unwarped_lines, 1, 0)

    return output_img

