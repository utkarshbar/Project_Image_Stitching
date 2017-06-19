def maxmin(pointsB,imageB):
        xmin=10000
        xmax=-1
        ct=len(pointsB)
        for k in range(0,ct,1):
        	if pointsB[k][0] > xmax :
        		xmax = pointsB[k][0]
        	if pointsB[k][0] < xmin :
        		xmin = pointsB[k][0]

        overlap =(float(xmin)/imageB.shape[1])

        print("overlap " + str(overlap))
        return overlap