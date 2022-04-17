Python 3.10.2 (tags/v3.10.2:a58ebcc, Jan 17 2022, 14:12:15) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
def fitting_polynomial(leftx, lefty, rightx, righty):
    """
    Given x and y coordinates of lane pixels fit 2nd order polynomial through them
    
    here the function is of y and not x that is
    
    x = f(y) = Ay**2 + By + C
    
    returns coefficients A, B, C for each lane (left lane and right lane)
    """
    # Fit a second order polynomial to each with np.polyfit()
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)

    return left_fit, right_fit