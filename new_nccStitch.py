import cv2
import numpy as np
import math

#res_max for storing highest correlation value, x for storing corresponding x coordimate, interval 

def nccStitch(imageA,imageB):
        res_max=-2
        
        interval=16
        z=min(imageA.shape[1],imageB.shape[1])
        h=min(imageB.shape[0],imageA.shape[0])
        w=int(z*0.2)
        print(imageA.shape[1])
        for i in range (int(imageA.shape[1]*0.8),imageA.shape[1]-16,interval):
                for k in range(0,imageA.shape[0]-16,64):
                        for j in range(0,w-16,interval):
                                for l in range(0,imageB.shape[0]-16,64):

                                        #Temp for storing the window size for A
                                        temp=imageA[k:k+16,i:i+16]

                                        #print(temp.shape[1])
                                        mean_A=np.mean(temp)
                                        imgA = temp-mean_A
                       
                                        #Template for storing the window size for 
                                        template = imageB[l:l+16,j:j+16]
                                        #print(template.shape[1])

                                        #calculation for cross correlation
                                        mean_B=np.mean(template)
                                        imgB = template-mean_B
                                        prod=imgA*imgB
                                        sumB=np.sum(prod)
                                        prodSquare=imgA*imgB*imgA*imgB
                                        sumSquare=math.sqrt(float(np.sum(prodSquare)))
                                        if(sumSquare==0):
                                                continue
                                        print("res_max: "+str(res_max))
                                        corr =(float(sumB)/sumSquare)/(temp.shape[0]*temp.shape[1])
                
                                        #compare correlation and  max correlation available yet and storing the corresponding width
                                        if(res_max < corr):
                                                res_max=corr
                                                
                                                
                                                xA1=i
                                                xB1=j
                                                yA1=k
                                                yB1=l


        #print("loop change")
        #croping image according the best possible correlation and leave start part of image because start rgion of image is black 
        overlap=(float(xA1+16)/imageA.shape[1])
        print("overlap: "+str(overlap))

       
        pointsA=[[xA1,yA1],[xA1+16,yA1],[xA1,yA1+16],[xA1+16,yA1+16]]
        pointsB=[[xB1,yB1],[xB1+16,yB1],[xB1,yB1+16],[xB1+16,yB1+16]]


        if(overlap < 1 and res_max >0 ):
                H,mask=cv2.findHomography(np.asarray(pointsB,float),np.asarray(pointsA,float),cv2.RANSAC,3)
                
                top_left=np.array([0.0,0.0,1.0])
                top_right=np.array([imageB.shape[1],0.0,1.0])
                bottom_right=np.array([imageB.shape[1],imageB.shape[0],1.0])
                bottom_left=np.array([0,imageB.shape[0],1.0])
                bottom_right_H=np.dot(H,bottom_right)
                top_right_H=np.dot(H,top_right)
                top_left_H=np.dot(H,top_left)
                bottom_left_H=np.dot(H,bottom_left)
               
                
                if(top_right_H[0]>bottom_right_H[0]):
                        width=int(top_right_H[0])
                else:
                        width=int(bottom_right_H[0])

                height=max(int(bottom_right_H[1])-int(top_right_H[1]),int(bottom_left_H[1])-int(top_left_H[1]),imageA.shape[0])   



                result = cv2.warpPerspective(imageB,H,(width, height))
                
                print(result.shape)

                result[0:imageA.shape[0],0:imageA.shape[1]]=imageA
                #imageB=cv2.resize(imageB,(imageB.shape[1],imageA.shape[0]))
                #img1=imageB[0:imageB.shape[0],xB:imageB.shape[1]]
                #img2=imageA[0:imageB.shape[0],0:xA]
                #result=np.concatenate((img2,img1),axis=1)
                
        else:
                imageB=cv2.resize(imageB,(imageB.shape[1],imageA.shape[0]))
                result=np.concatenate((imageA,imageB),axis=1)
        
        #concatenate the image portions horizontally 
        
        return result
'''
imageA=cv2.imread("Clips/3_4/image_235.jpg",0)
imageB=cv2.imread("Clips/3_4/image_236.jpg",0)
r=nccStitch(imageA,imageB)
cv2.imwrite('x.jpg',r)
'''