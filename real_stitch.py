import cv2
import numpy as np
from v2f import vid2Frame
from image_stitch import stitch
from new_nccStitch import nccStitch
'''
inputVid="ImageStitching.wmv"
outVidLoc="IM"
count=vid2Frame(inputVid,outVidLoc)

'''
outVidLoc="image_"
interval =1
count=9
imageA=cv2.imread(str(outVidLoc)+ str(500)+".jpg",0)
for j in range(1,count, interval):
         imageB=cv2.imread(str(outVidLoc)+ str(500-j)+".jpg",0)
         print(j)
         result=stitch(imageA,imageB)
         imageA=result
         cv2.imwrite("k_"+str(j)+".jpg",result)
         
cv2.imwrite('2.jpg', result)