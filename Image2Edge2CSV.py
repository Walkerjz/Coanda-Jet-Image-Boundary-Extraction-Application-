import cv2
import time
import numpy as np

#FilePath is the image you are edge detecting.
FilePath = 'Data/1800um/'
FileName = 'rcphoto1810um21psi_2019.jpg'
#TarePath is the lowest pressure image.
TareName = 'rcphoto1810um5psi_2019.jpg'
# some other files ['Data/1800um/Tare1810um10psi.jpg','Data/1800um/Tare1810um15psi.jpg','Data/1800um/Tare1810um20psi.jpg','Data/1800um/Tare1810um21psi.jpg']
Mask = 'Data/1800um/UniversalMask2.jpg'

#Read images and convert them to a gray scale format so the matrix is 2D not 3D
File = cv2.cvtColor(cv2.imread(FilePath+FileName), cv2.COLOR_BGR2GRAY)
Tare = cv2.cvtColor(cv2.imread(FilePath+TareName), cv2.COLOR_BGR2GRAY)
Mask = cv2.cvtColor(cv2.imread(Mask), cv2.COLOR_BGR2GRAY)

Diff = cv2.subtract(File, Tare)
image = cv2.subtract(Diff,Mask)

#canny thresholds of 0 and 207 work for the psipath files to answer question 3 and a filter d=5
# d=12 works well for Data/rcphoto2370um30psi_2019.jpg
def apply_canny(image, low_threshold, high_threshold):
    """Applies Canny edge detection with adjustable thresholds."""
    # Apply Canny edge detection
    #filter the image
    filt = cv2.bilateralFilter(image,d=5, sigmaColor=1000, sigmaSpace=75)
    #apply the canny image detection and return image of the edges found
    edges = cv2.Canny(filt, low_threshold, high_threshold, apertureSize=5)
    # return the grayscale image and edges
    return edges

def extract_edges(edges):
    '''This function takes a canny edge detection file and returns the right-most edges arrays of X and Y coordinates'''
    #create arrays for X and Y coordinates
    edgeX = []
    edgeY = []
    #start from y = 260 and iterate through rows until row 316. These values are adjustable to avoid unwanted edge artifacts
    i = 260
    while i<316:
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

print('the X coordinates ' + str(X))
print('the Y coordinates ' + str(Y))
a=np.array([X,Y])
np.savetxt(FileName,a, delimiter=",")

cv2.destroyAllWindows()