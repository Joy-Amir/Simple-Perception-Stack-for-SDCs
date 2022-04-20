import numpy as np
import cv2

#here we will fit a seconed order polynomial between the pixels of the lane and draw the lane 
def fit_and_draw_lane(leftx, lefty, rightx, righty, left_fit, right_fit, img, first_run):
    # Fit a second order polynomial to each with np.polyfit()
    if len(lefty) > 1500 or first_run:
        left_fit = np.polyfit(lefty, leftx, 2)
    if len(righty) > 1500 or first_run:
        right_fit = np.polyfit(righty, rightx, 2)

    # Generate x and y values for plotting
    maxy = img.shape[0] - 1  # getting the max height of the image
    miny = img.shape[0] // 3  # taking the min to be the floor of third the height
    if len(lefty):  # getting max and min of left lane height along with the previously assumed max and min above
        maxy = max(maxy, np.max(lefty))
        miny = min(miny, np.min(lefty))

    if len(righty):  # getting max and min of right lane height along with the previously assumed/calc max and min above
        maxy = max(maxy, np.max(righty))
        miny = min(miny, np.min(righty))

    # Generate y values then calculate x values from polynomial function
    ploty = np.linspace(miny, maxy, img.shape[0])
    left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
    right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]

    # Visualization
    out_img = np.dstack((img, img, img))  # converting them to 3 channels

    # match a straight line between every 2 points in front of each other in the right and left lanes with green line
    for i, y in enumerate(ploty):
        l = int(left_fitx[i])
        r = int(right_fitx[i])
        y = int(y)
        cv2.line(out_img, (l+7, y), (r-7, y), (0, 255, 0))
        cv2.line(out_img, (l-6, y), (l+6, y), (255, 0, 0))
        cv2.line(out_img, (r-6, y), (r+6, y), (0, 0, 255))

    return left_fit, right_fit, out_img
