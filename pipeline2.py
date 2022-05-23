import numpy as np
from copy import copy
import cv2
from find_cars import find_cars
from heatmap import generate_heatmap, draw_bboxes
from debug_mode2 import debug_mode
from draw_detected import draw_thumbnails, draw_background_highlight

bboxes = []
i = 1

# Parameters for junshengfu_heatmap
Heatmap_buffer = []
N_buffer = 3
heatmap_pre = 0
mask = 0


def pipeline2(image, test_images, debug_mode_on):
    global bboxes
    global i
    global heatmap_pre
    global mask
    global clipped

    if i or test_images:  # test_images: to not drop frames in case of testing images

        windows_list = find_cars(np.copy(image))
        heatmap_pre = generate_heatmap(image, windows_list)
        output_image, heatmap_post, bboxes, mask = draw_bboxes(np.copy(image), copy(Heatmap_buffer), heatmap_pre,
                                                    min(len(Heatmap_buffer) + 1, N_buffer), bboxes, i or test_images, mask)
        i = 0
        if len(Heatmap_buffer) >= N_buffer:
            Heatmap_buffer.pop(0)

    else:

        for bbox in bboxes:
            # Draw the box on the image
            cv2.rectangle(image, bbox[0], bbox[1], (0, 0, 255), 4)
        output_image = image
        i = 1

    output_image = draw_background_highlight(output_image)
    draw_thumbnails(output_image, bboxes)
    if debug_mode_on and len(bboxes) > 0:
        output_image = debug_mode(output_image, mask)
    return output_image
