import cv2
import time
import numpy as np

'''
This program takes Scherien Images of Coanda Jets and extracts the jet boundary using canny edge detection.
To use this program change the file name and run the program. Adjust the sliders until the edge detection looks good 
then press 'q' to exit and save the points as a csv with the same name as the image file.

Adjustable functions:
-Change directory file path
-change file name
-change background image
-change mask file
-change bilateral filter
-change canny edge detection aperture size 
-The i and bottom values methods determine where the top and bottom pixels that are extracted.
'''

#FilePath is the directory you are pulling from
FilePath = 'Data/'
#file Name is the image we want to extract the boundary from
FileName = 'rcphoto1810um21psi_2019'
#TarePath is a background image.
# In the absence of a background image use the lowest pressure in a slot width set you are testing
TareName = 'rcphoto1810um5psi_2019'
# The mask file was created using ImageJ. It is used here to get rid of random flow phenomena
#floating around in the fluid flow
Mask = 'UniversalMask2.jpg'

#Read images and convert them to a gray scale format so the matrix is 2D not 3D
File = cv2.cvtColor(cv2.imread(FilePath+FileName+'.jpg'), cv2.COLOR_BGR2GRAY)
Tare = cv2.cvtColor(cv2.imread(FilePath+TareName+'.jpg'), cv2.COLOR_BGR2GRAY)
Mask = cv2.cvtColor(cv2.imread(Mask), cv2.COLOR_BGR2GRAY)

#Subtract the background from the image to boost contrast
Diff = cv2.subtract(File, Tare)
# use the mask to get rid of random flow phenomena
# floating around in the fluid flow
image = cv2.subtract(Diff,Mask)


def apply_canny(image, low_threshold, high_threshold):
    """Applies Canny edge detection and a bilateral filter with adjustable thresholds."""
    #The bilateral filter filters the image while maintaining edges
    #sigmacolor shouldn't do much because we are only using one color
    # you can read more here https://www.geeksforgeeks.org/python-bilateral-filtering/
    filt = cv2.bilateralFilter(image,d=5, sigmaColor=1000, sigmaSpace=75)
    #apply the canny image detection and returns the image of the edges found
    edges = cv2.Canny(filt, low_threshold, high_threshold, apertureSize=5)
    # return the edges
    return edges

def extract_edges(edges):
    '''This function takes a canny edge detection file and returns the right-most edges arrays of X and Y coordinates'''
    #create arrays for X and Y coordinates
    edgeX = []
    edgeY = []
    #start from y = 260 and iterate through rows until row 316. These values are adjustable to avoid unwanted edge artifacts
    i = 260
    bottom = 316
    while i<bottom:
        # start from the right of the image and iterate across
        j = 605
        while j>=0:
            #if reach a pixel that is 255 that's an edge so save in the appropriate arrays and break out of the loop
            if edges[i,j] == 255:
                #save coordinate in appropriate array
                edgeX.append(j)
                edgeY.append(i)
                break
            else:
                #decreasing because scanning from right to left
                j=j-1
        #increasing because scanning down the image (image origin in the top left corner)
        i=i+1
    #return the edge coordinates
    return edgeX, edgeY

# Create a window with trackbars
cv2.namedWindow('Canny Edge Detection (Press Q to leave)')
cv2.createTrackbar('Low Threshold', 'Canny Edge Detection (Press Q to leave)', 0, 255, lambda x: x)
cv2.createTrackbar('High Threshold', 'Canny Edge Detection (Press Q to leave)', 0, 255, lambda x: x)
while True:
    # Get the current trackbar values
    low_threshold = cv2.getTrackbarPos('Low Threshold', 'Canny Edge Detection (Press Q to leave)')
    high_threshold = cv2.getTrackbarPos('High Threshold', 'Canny Edge Detection (Press Q to leave)')

    # Apply Canny edge detection
    edges = apply_canny(image, low_threshold, high_threshold)

    # Display the result adding the gray image and edges
    cv2.imshow('Canny Edge Detection (Press Q to leave)', cv2.add(edges,File))

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        X,Y = extract_edges(edges)
        break
#print the X and Y coordinates
print('the X coordinates ' + str(X))
print('the Y coordinates ' + str(Y))

#save the array to a csv
a=np.array([X,Y])
np.savetxt(FileName+'.csv',a, delimiter=",")

#close the window
cv2.destroyAllWindows()