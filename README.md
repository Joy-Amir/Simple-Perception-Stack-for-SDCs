# Simple Perception Stack For Self-Driving Cars
In this project, a perception stack for self-driving cars is created. <br />
The project deals with video streams from cameras. <br />
The lane lines are to be detected. In addition, the car offset and the radius of curvature are calculated. <br />
<br />
## Pipeline Stages 
1. Camera calibration and distortion correction.<br />
2. Perspective transform.<br />
3. Color thresholding.<br />
4. Lane pixels detection using sliding window.<br />
5. A second order polynomial fitting to found pixels of each lane.<br />
6. Lanes colouring.<br />
7. Car offset and the radius of curvature calculation.<br />
8. Inverse perspective transform.<br />
## How to run the project
1. Open the command line prompt.<br />
2. Run the shell script "test.sh" with the following arguments in order:<br />
    a. The input_video_path.<br />
    b. The output_video_path.<br />
    c. 1 for debug mode and 0 otherwise.<br />
#### Illustrative examples
      - For debug mode type: sh test.sh ./project_video.mp4 ./result.mp4 1
      - For normal mode type: sh test.sh ./project_video.mp4 ./result.mp4 0
