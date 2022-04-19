# Simple Perception Stack for Self-Driving Cars
In this project we are creating a perception stack for self-driving cars.
we’re  focusing on video streams from cameras. 
We’re detecting the lane lines.
..............................................................................
our pipeline does the follow .
Camera calibration and correcting the distortion.
Perspective transform.
Color thresholding.
Finding the lane pixels using sliding windows.
Fitting a second order polynomial to the found lane pixels.
Drawing the lane.
Calculate the car offset and the radius of curvature.
Inverse perspective transform.
