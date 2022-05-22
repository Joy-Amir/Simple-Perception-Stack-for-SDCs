from scipy.ndimage.measurements import label
import numpy as np
import cv2
import matplotlib.pyplot as plt

buffer_weights = [0.1, 0.2, 0.3, 0.4]


def generate_heatmap(image, windows_list):
    heat = np.zeros_like(image[:, :, 0]).astype(np.float)  # use blank dark image
    # Add heat to each box in box list
    heat = add_heat(heat, windows_list)
    # Apply threshold to help remove false positives
    heat = apply_threshold(heat, 1)
    # Visualize the heatmap when displaying
    heatmap = np.clip(heat, 0, 255)

    return heatmap


def add_heat(heatmap, bbox_list):
    # Iterate through list of bboxes
    for box in bbox_list:
        # Add += 1 for all pixels inside each bbox
        # Assuming each "box" takes the form ((x1, y1), (x2, y2))
        heatmap[box[0][1]:box[1][1], box[0][0]:box[1][0]] += 1      # box[0][1]:y1     box[1][1]:y2

    # Return updated heatmap
    return heatmap  # Iterate through list of bboxes


def apply_threshold(heatmap, threshold):
    # Zero out pixels below the threshold
    heatmap[heatmap <= threshold] = 0       # threshold is determined as 1 or 2
    # Return thresholded map
    return heatmap


# New-------------------------------------------------------------------------------------------------------------------
def draw_boxes(img, bboxes, color=(0, 0, 255), thick=6):
    out_img = np.copy(img)
    for b in bboxes:
        cv2.rectangle(out_img, *b, color, thick)  # drawing rectangle that is found in the pointer
    return out_img

# -----------------------------------------------------------------------------------------------------------------------


def draw_bboxes(img, heatmap_buffer, heatmap_pre, N_buffer, prev_bboxes, new_frame, mask):
    if new_frame:
        heatmap_buffer.append(heatmap_pre)

        if len(heatmap_buffer) > N_buffer:  # remove the first component if it is more than N_buffer elements
            heatmap_buffer.pop(0)

        # weight the heatmap based on current frame and previous N frames
        idxs = range(N_buffer)
        for b, w, idx in zip(heatmap_buffer, buffer_weights, idxs):
            heatmap_buffer[idx] = b * w

        heatmap = np.sum(np.array(heatmap_buffer), axis=0)
        heatmap = apply_threshold(heatmap, threshold=sum(buffer_weights[0:N_buffer])*2)

        # Find final boxes from heatmap using label function
        labels = label(heatmap)

        bboxes = []
        # locate the bounding box
        for car_number in range(1, labels[1]+1):
            # Find pixels with each car_number label value
            nonzero = (labels[0] == car_number).nonzero()
            # Identify x and y values of those pixels
            nonzeroy = np.array(nonzero[0])
            nonzerox = np.array(nonzero[1])
            # Define a bounding box based on min/max x and y
            bbox_tmp = ((np.min(nonzerox), np.min(nonzeroy)), (np.max(nonzerox), np.max(nonzeroy)))
            bboxes.append(bbox_tmp)

        # New ---------------------------------------------------------------------------------------------------------
        out = np.copy(img)

        # creating a mask having only the blue boxes with thickness =
        mask = draw_boxes(np.zeros_like(img), bboxes=bboxes, thick=-1)

        # returning contours of the bounded boxes by passing the B channel only
        contours, _ = cv2.findContours(mask[:, :, 2].astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for countour in contours:
            x, y, width, height = cv2.boundingRect(countour)
            cv2.rectangle(out, (x, y), (x + width, y + height), (0, 0, 255), 4)

        # -------------------------------------------------------------------------------------------------------------------

    else:
        out = img
        heatmap = 0
        bboxes = []
    # Return the image
    return out, heatmap, bboxes, mask
