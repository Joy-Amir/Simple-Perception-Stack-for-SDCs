from calibrate import undistort_image
def pipeline(image):
    image = undistort_image(image)                      # correct camera distortion
    #######Call your processing functions on image: image = function_name(image)
    return image

