import numpy as np
import cv2
#we will find the image form a bird eye view perspective
def perspective_transform(binary_img):  #this function takes a binary image
    srcpoints = np.float32([(550, 460),(150, 720),(1200, 720),(770, 460)])  #we specify any four points in the image as a source points
    dstpoints = np.float32([(100, 0),(100, 720),(1100, 720),(1100, 0)])     #we also specify  a four points of a rectangle as a distinatiton points

    img_size = (binary_img.shape[1], binary_img.shape[0]) #we specify the binary image size

    M = cv2.getPerspectiveTransform(srcpoints, dstpoints) #matrix

    warped_image = cv2.warpPerspective(binary_img, M, img_size, flags=cv2.INTER_LINEAR) #make the perspective

    return warped_image

# we will return back to the driver view 
def inv_perspective_transform(binary_img):  #we'll give it also a binary image
    dstpoints = np.float32([(550, 460),(150, 720),(1200, 720),(770, 460)])   #we specifiy the four points in the image we specified before in the source as destination
    srcpoints = np.float32([(100, 0),(100, 720),(1100, 720),(1100, 0)])      #and we also specify the rectangle points as a source points

    img_size = (binary_img.shape[1], binary_img.shape[0])   #we specify the binary image sizes

    Minv = cv2.getPerspectiveTransform(srcpoints, dstpoints)  #inverse matrix

    warped_image = cv2.warpPerspective(binary_img, Minv, img_size, flags=cv2.INTER_LINEAR) #make the inverse perspective

    return warped_image
