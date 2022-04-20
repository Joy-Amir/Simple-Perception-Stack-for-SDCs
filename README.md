# Simple Perception Stack for Self-Driving Cars
In this project we are creating a perception stack for self-driving cars.
we’re  focusing on video streams from cameras. 
We’re detecting the lane lines.
....
our pipeline does the follow .
Camera calibration and correcting the distortion.
Perspective transform.
Color thresholding.
Finding the lane pixels using sliding windows.
Fitting a second order polynomial to the found lane pixels.
Drawing the lane.
Calculate the car offset and the radius of curvature.
Inverse perspective transform.
<!-- how to run the project -->
open the command line :
run the shell script "test.sh" with passing the input_video_path as the  first argument , output_video_path as the seconed argument and 0 or 1 as the third argument (with space between the arguments).
type sh test.sh input_video_path output_video_path 0
or 
sh test.sh input_video_path output_video_path 1
you can choose 0 for debuging mode
and 1 for no debuging mode

