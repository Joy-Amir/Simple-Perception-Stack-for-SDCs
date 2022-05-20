import numpy as np
import cv2


def draw_background_highlight(image):

    mask = cv2.rectangle(np.copy(image), (0, 0), (image.shape[1], 155), (0, 0, 0), thickness=cv2.FILLED)
    draw_img = cv2.addWeighted(src1=mask, alpha=0.3, src2=image, beta=0.8, gamma=0)

    return draw_img


def draw_thumbnails(img, window_list):

    cv2.putText(img, 'Detected Vehicles', (4, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2, cv2.LINE_AA)
    for i, bbox in enumerate(window_list):
        thumbnail = img[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
        vehicle_thumb = cv2.resize(thumbnail, dsize=(100, 80))
        start_x = 300 + (i+1) * 30 + i * 100
        img[60:140, start_x:start_x + 100, :] = vehicle_thumb
