import cv2
import time
import numpy as np

def extract_Flare_edges(File):
    '''This function takes a canny edge detection file and returns the right-most edges arrays of X and Y coordinates'''
    #create arrays for X and Y coordinates
    edgeX = []
    edgeY = []

    i =0
    bottom = 334
    while i<bottom:
        # start from the left of the image and iterate across
        j = 0
        while j<=605:
            #if reach a pixel that isn't 0 that's an edge so save in the appropriate arrays and break out of the loop
            if File[i,j] >= 35:
                #save coordinate in appropriate array
                edgeX.append(j)
                edgeY.append(i)
                break
            else:
                #decreasing because scanning from right to left
                j=j+1
        #increasing because scanning down the image (image origin in the top left corner)
        i=i+1
    #return the edge coordinates
    return edgeX, edgeY


FilePath = 'Data/'
FileName = 'rcphoto1810um21psi_2019'
File = cv2.cvtColor(cv2.imread(FilePath+FileName+'.jpg'), cv2.COLOR_BGR2GRAY)
X,Y = extract_Flare_edges(File)
print('the X coordinates ' + str(X))
print('the Y coordinates ' + str(Y))



