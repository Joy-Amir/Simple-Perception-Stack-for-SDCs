import numpy as np

def measure_center_curvature(left_fit_coef, right_fit_coef, image_shape):
    """
    It takes the polynomial functions and original image dimensions.
    It calculates the offset of the car from the center of the lanes and the curvature in meters.
    It returns the offset and a direction the car to go to and the right and left curvature of the road.
    """

    # Conversions from pixels to meters
    ym_per_pix = 30/720  # meters per pixel in y dimension
    xm_per_pix = 3.7/700  # meters per pixel in x dimension

    ############ Calculating the car offset
    # Get the position of the car (in the middle of the image)
    car_center_x = image_shape[1] / 2  # the middle of the x_axis range

    # Get the x dimension of the center between the two lanes at the bottom of the image
    # by substituting in the 2nd order polynomial curve x = Ay^2 + By + C
    # where y is the maximum value at the bottom of the page
    left_lane_bottom_x = left_fit_coef[0] * (image_shape[0] ** 2) + left_fit_coef[1] * image_shape[1] + left_fit_coef[2]
    right_lane_bottom_x = right_fit_coef[0] * (image_shape[0] ** 2) + right_fit_coef[1] * image_shape[1] + \
                          right_fit_coef[2]
    lane_center_x = (left_lane_bottom_x + right_lane_bottom_x) / 2

    # Get the car_offset i.e the difference between the lane_center and car_center
    car_offset = (lane_center_x - car_center_x) * xm_per_pix  # in meters
    car_offset = round(car_offset, 3)

    # Get the direction of the car offset
    direction = ""
    if car_offset > 0:
        direction = "Go right"
    elif car_offset < 0:
        direction = "Go left"
    else:
        direction = "Stay put"

    car_offset = np.absolute(car_offset)


    ############ Calculating the radius of curvature
    # Get the y (vertical, first dimension in image_shape) value where the curvature should calculated
    y_eval = image_shape[0]  # the maximum value i.e the bottom of the image

    # Calculation of radius of curvature of 2nd order polynomial using the formula R = (1 + (2Ay + B)^2)^(3/2) / (|2A|)
    # where A and B are the polynomial coefficients 0 and 1 respectively
    # y is y_eval (where the radius should be calculated) * ym_per_pix to be in meters
    left_curve_rad = ((1 + (2*left_fit_coef[0]*y_eval*ym_per_pix + left_fit_coef[1])**2)**(3.0/2)) / np.absolute(2*left_fit_coef[0])
    right_curve_rad = ((1 + (2*right_fit_coef[0]*y_eval*ym_per_pix + right_fit_coef[1])**2)**(3.0/2)) / np.absolute(2*right_fit_coef[0])
    curvature = (left_curve_rad + right_curve_rad) / 2.0
    curvature = round(curvature, 3)

    return str(car_offset), direction, str(curvature)
