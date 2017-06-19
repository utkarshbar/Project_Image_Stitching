import cv2
import numpy as np
from min_max import maxmin
from new_nccStitch import nccStitch
from combine_vertical import vertical

def stitch_L2R(imageA,imageB):
        s = cv2.ORB_create(5000)
        
        (kpsA, featuresA) = s.detectAndCompute(imageA,None)
        (kpsB, featuresB) = s.detectAndCompute(imageB,None)

        if(len(kpsA)<=4 or len(kpsB)<=4):
                result=nccStitch(imageB,imageA)
                return result

        bf = cv2.BFMatcher()
        rawMatches = bf.knnMatch(featuresA,featuresB,k=2)
        matches = []
        for m in rawMatches:
                if len(m) == 2 and m[0].distance < m[1].distance * 0.75:
                                matches.append((m[0].trainIdx, m[0].queryIdx))

        
        
        pointsA=np.float32([kpsA[k].pt for (_,k) in matches])
        pointsB=np.float32([kpsB[t].pt for (t,_) in matches])

        if(len(pointsA)<=4 or len(pointsB)<=4):
                result=nccStitch(imageA,imageB)
                return result
        
        print("pointsA: "+str(len(pointsA)))
        print("pointsB: "+str(len(pointsB)))
        print("pointsA")
        print(pointsA)

        print("pointsB")
        print(pointsB)

        overlap=maxmin(pointsB,imageB)
        #H,mask=cv2.findHomography(pointsA,pointsB,cv2.RANSAC,3)

      
        imageB=cv2.resize(imageB,(imageB.shape[1],imageA.shape[0]))
        #result = cv2.warpPerspective(imageA,H,(int(imageA.shape[1]*overlap + imageB.shape[1]),imageA.shape[0]))
        
        #result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
       
        img1=imageA[0:imageB.shape[0], int(imageB.shape[1]*(overlap)):imageA.shape[1]]
       

        result =np.concatenate((imageB,img1),axis=1)
        
        return result
        

def stitch_R2L(imageA,imageB):
        s = cv2.ORB_create(10000)
        (kpsA, featuresA) = s.detectAndCompute(imageA,None)
        (kpsB, featuresB) = s.detectAndCompute(imageB,None)
        result=nccStitch(imageB,imageA)
        return result
        if(len(kpsA)<=4 or len(kpsB)<=4):
                result=nccStitch(imageB,imageA)
                return result


        bf = cv2.BFMatcher()
        matches = bf.knnMatch(featuresA,featuresB,k=3)


        
        pairsOfKp1 = [i[0].queryIdx for i in matches]
        pairsOfKp2 = [i[0].trainIdx for i in matches]
        pointsA=np.array([kpsA[k].pt for k in pairsOfKp1], np.float32)
        pointsB=np.array([kpsB[t].pt for t in pairsOfKp2], np.float32)

        if(len(pointsA)<=4 or len(pointsB)<=4):
                result=nccStitch(imageB,imageA)
                return result


        overlap=maxmin(pointsB,imageB)
        H,mask=cv2.findHomography(pointsA,pointsB,cv2.RANSAC,3)
        #imageB=cv2.resize(imageB,(imageB.shape[1],imageA.shape[0]))
        result = cv2.warpPerspective(imageA,H,(int(imageA.shape[1] + (1-overlap)*imageB.shape[1]), imageB.shape[0]+imageA.shape[0]))
        result[0:imageB.shape[0],0:imageB.shape[1]]=imageB
        #img1=imageB[0:imageB.shape[0], 0:int(imageB.shape[1]-imageA.shape[1]*overlap)]
        #result=np.concatenate((img1,imageA),axis=1)
       
        return result