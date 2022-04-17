import numpy as np
import cv2

class Lane:
    def __init__(self):

        self.nwindows = 9                                               # Number of sliding windows
        self.window_height = None
        self.margin = 100                                               # The width of the window:margin .centre. margin
        self.minpix = 50            #200                                # The minimum number of found pixels in the window to recenter it
        self.nonzero = None
        self.nonzerox = None
        self.nonzeroy = None
        self.image = None

    def in_window(self, center, margin, height):                         # Check that a certain point is in the window
        leftx = center[0] - margin
        rightx = center[0] + margin
        upy = center[1] - height // 2
        downy = center[1] + height // 2

        x_inside = (self.nonzerox >= leftx) & (self.nonzerox <= rightx)
        y_inside = (self.nonzeroy >= upy) & (self.nonzeroy <= downy)
        return self.nonzerox[x_inside & y_inside], self.nonzeroy[x_inside & y_inside]

    def initialize_variables(self, image):
        self.image = image
        self.nonzero = image.nonzero()                # Return a tuple of arrays for each dimension including the indices of nonzero elements
        self.nonzerox = np.array(self.nonzero[1])     # Equivalent to self.nonzero[1]
        self.nonzeroy = np.array(self.nonzero[0])
        self.window_height = np.int(image.shape[0] // self.nwindows)

    def histogram(self, image):
        bottom_image = image[image.shape[0] // 2:,:]                    # Extract the bottom half of the image where the lanes lie
        return np.sum(bottom_image, axis = 0)                           # Sum the intensities over the y-axis for each x

    def find_lanes(self, image):
        self.initialize_variables(image)
        h = self.histogram(image)
        midx = h.shape[0] // 2
        left_x = np.argmax(h[: midx])                                    # Get the x of maximum histogram value in the left
        right_x = np.argmax(h[midx: ]) + midx                            # Get the x of maximum histogram value in the right
        y = image.shape[0] + self.window_height // 2                    # Required so that when we enter the for loop the
                                                                        # initial y is image.shape[0] - self.window_height // 2

        leftx, lefty, rightx, righty = [], [], [], []                   # Empty lists for the left and right lane pixels
        for window in range(self.window_height):
            y = y - self.window_height
            left_center = (left_x, y)
            right_center = (right_x, y)
            #print(left_center[0], self.margin)
            left_x_inwindow , left_y_inwindow = self.in_window(left_center, self.margin, self.window_height)
            right_x_inwindow, right_y_inwindow = self.in_window(right_center, self.margin, self.window_height)
            # Extends the list with the found indices in the window
            leftx.extend(left_x_inwindow)
            lefty.extend(left_y_inwindow)
            rightx.extend(right_x_inwindow)
            righty.extend(right_y_inwindow)
            # Recenter the window
            if len (left_x_inwindow) > self.minpix:
                left_x = np.int32(np.mean(left_x_inwindow))
            if len (right_x_inwindow) > self.minpix:
                right_x = np.int32(np.mean(right_x_inwindow))

        return leftx, lefty, rightx, righty

    def search_around_poly(self, leftpoly, rightpoly):
        self.initialize_variables(image)
        margin = 100
        # if the lane has no abrupt curves, then we would expect the lane to be close to the previous found lane
        # Substitute by the lane equation using y points and check if the corresponding x points lies within a certain margin
        # If so, then this points are part of the lane and use them to calculate the new lane polynomial
        left_lane_indices = \
            ((self.nonzerox > (leftpoly[0] * (self.nonzeroy**2) + leftpoly[1] * (self.nonzeroy) + leftpoly[2]-margin))
             &(self.nonzerox < (leftpoly[0] * (self.nonzeroy**2) + leftpoly[1] * (self.nonzeroy) + leftpoly[2]+margin))
             ).nonzero()[0]

        right_lane_indices = \
        ((self.nonzerox > (rightpoly[0] * (self.nonzeroy ** 2) + rightpoly[1] * (self.nonzeroy) + rightpoly[2] - margin))
         & (self.nonzerox < (rightpoly[0] * (self.nonzeroy ** 2) + rightpoly[1] * (self.nonzeroy) + rightpoly[2] + margin))
         ).nonzero()[0]

        leftx = self.nonzerox[left_lane_indices]
        lefty = self.nonzeroy[left_lane_indices]
        rightx = self.nonzerox[right_lane_indices]
        righty = self.nonzeroy[right_lane_indices]

        return leftx, lefty, rightx, righty





# Testing
l = Lane()
image = cv2.imread('road.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
l.find_lanes(image)