import cv2

def write_text(img, offset, direction, curvature):
    # writing the offset, curvature and direction
    cv2.putText(img, "Offset from center = " + offset + " m", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1,
                (0, 255, 200), 1)
    cv2.putText(img, direction, (10, 90), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 200), 1)
    cv2.putText(img, "Radius of curvature = " + curvature + " m", (10, 130), cv2.FONT_HERSHEY_DUPLEX, 1,
                (0, 255, 200), 1)
    return img