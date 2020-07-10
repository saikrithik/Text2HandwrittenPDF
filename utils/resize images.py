import os
import re, os.path
import cv2

mypath = "letterimages"
for root, dirs, files in os.walk(mypath):
    for file in files:
        ImageName = os.path.join(root, file)
        print()
        src = cv2.imread(cv2.samples.findFile(ImageName), cv2.IMREAD_COLOR)
        image = cv2.resize(src, (40,120))
        cv2.imwrite(ImageName[:-3]+"png", image)
        
