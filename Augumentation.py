from matplotlib import pyplot as plt
import numpy as np
import cv2
import math
import random
import copy
import imutils
def translation(src,y):
    if int(random.uniform(0, 2)):
        x=0
        y = int(random.uniform(-y, y))
        M = np.float32([[1, 0, x], [0, 1, y]])
        src = cv2.warpAffine(src, M, (src.shape[1], src.shape[0])
                                 ,borderValue=(255,255,255))
    return src
    
def zoom(src,zoom_thresh_up,zoom_thresh_down):
    scaledownX = random.uniform(zoom_thresh_down,1)
    scaledownY = random.uniform(zoom_thresh_down,1)
    scaleupX = random.uniform(1,zoom_thresh_up)
    scaleupY = random.uniform(1,zoom_thresh_up)
    if int(random.uniform(0,2)):
        src = cv2.resize(src, None, fx= scaledownX, fy= scaledownY,
                         interpolation= cv2.INTER_LINEAR)
    else:
        src = cv2.resize(src, None, fx= scaleupX, fy= scaleupY,
                         interpolation= cv2.INTER_LINEAR)
    return src
def warpAffine(src, M, dsize, from_bounding_box_only=False):
    """
    Applies cv2 warpAffine, marking transparency if bounding box only
    The last of the 4 channels is merely a marker. It does not specify opacity in the usual way.
    """
    return cv2.warpAffine(src, M, dsize,borderValue=(255,255,255))
def rotate_image(image, angle):
    """Rotate the image counterclockwise.
    Rotate the image such that the rotated image is enclosed inside the
    tightest rectangle. The area not occupied by the pixels of the original
    image is colored black.
    Parameters
    ----------
    image : numpy.ndarray
        numpy image
    angle : float
        angle by which the image is to be rotated. Positive angle is
        counterclockwise.
    Returns
    -------
    numpy.ndarray
        Rotated Image
    """
    # get dims, find center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    image = warpAffine(image, M, (nW, nH), False)

    # image = cv2.resize(image, (w,h))

    return image
