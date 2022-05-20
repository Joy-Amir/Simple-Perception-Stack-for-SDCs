# Simple Perception Stack For Self-Driving Cars
In this project, a perception stack for self-driving cars is created. <br />
The project deals with video streams from cameras. <br />
#### Phase 1:
&nbsp;&nbsp;&nbsp; The lane lines are to be detected. In addition, the car offset and the radius of curvature are calculated. <br />
#### Phase 2:
&nbsp;&nbsp;&nbsp; The cars are to be detected and bounded by rectangles. <br />
<br />
## Lane Detection Pipeline Stages 
1. Camera calibration and distortion correction.<br />
2. Perspective transform.<br />
3. Color thresholding.<br />
4. Lane pixels detection using sliding window.<br />
5. A second order polynomial fitting to found pixels of each lane.<br />
6. Lanes colouring.<br />
7. Car offset and the radius of curvature calculation.<br />
8. Inverse perspective transform.<br />
## Cars Detection Training Stages
1. Feature extraction using HOG, spatial and colour features.<br />
2. Feature normalization to speed up the training.<br />
3. Classifier training using multi-layer perceptron and support vector machines.<br />
#### Classifiers Accuracy:
|         | **MLP**  | **SVM**  |
| :---:   | :---: | :---: |
| **Training Accuracy** | 1.0 | 1.0 |
| **Testing Accuracy** | 0.996 | 0.9878 |
## Car Detection Pipeline Stages
1. Sliding windows of different sizes over the image.<br />
2. Features extraction for each window.
3. Applying the classifier to each window.
## How to run the project
1. Open the command line prompt.<br />
2. Run the shell script "test.sh" with the following arguments in order:<br />
    a. The input_video_path.<br />
    b. The output_video_path.<br />
    c. The phase to be tested: 1 for phase one and 2 for phase two.<br />
    d. 1 for debug mode and 0 otherwise.<br />
#### Illustrative examples
      - For debug mode type of phase 1: sh test.sh ./project_video.mp4 ./result.mp4 1 1
      - For normal mode type of phase 2: sh test.sh ./project_video.mp4 ./result.mp4 2 0

