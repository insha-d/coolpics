import cv2
import pywhatkit
import numpy as np
import os

def readImg(filename):
    img= cv2.imread(filename)
    return img
def edgeDetection(img, line_wdt,blur):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    grayblur= cv2.medianBlur(gray,blur)
    edges= cv2.adaptiveThreshold(grayblur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,line_wdt,blur)
    return edges
def color (img,k):
    data = np.float32(img).reshape((-1,3))
    criteria = (cv2.TermCriteria_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,0.001)
    ret, label, center = cv2.kmeans(data,k,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result
def resolveFile(name):
    path = os.path.dirname(__file__)
    resolved = os.path.join(path, "static","uploads",name)
    return resolved


# FOR SKETCH DRAWING
def sketch(sourceFile):
    img = readImg(resolveFile(sourceFile))
    line_wdt =9
    blur_value = 7
    totalColor = 4
    grayFilter = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(grayFilter)
    blur = cv2.GaussianBlur(invert, (21,21),0)
    invvertedBlur = cv2.bitwise_not(blur)

    sketch = cv2.divide(grayFilter,invvertedBlur,scale=256.0)
    cv2.imwrite(resolveFile(sourceFile.replace(".","_sketch.")),sketch)

# FOR BLACK AND WHITE
def bnw(sourceFile):
    img = readImg(resolveFile(sourceFile))
    line_wdt =9
    blur_value = 7
    totalColor = 4
    grayFilter = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(resolveFile(sourceFile.replace(".","_bw.")),grayFilter)

# FOR CARTOON 
def cartoon(sourceFile):
    img = readImg(resolveFile(sourceFile))
    line_wdt =5
    blur_value = 5
    totalColor = 16
    grayFilter = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edgeImg = edgeDetection(img,line_wdt,blur_value) 
   
    img= color(img,totalColor)

    blurred = cv2.bilateralFilter(img, d=4,sigmaColor=400,sigmaSpace=400)
    cartoon = cv2.bitwise_and(blurred,blurred,mask=edgeImg)
    cv2.imwrite(resolveFile(sourceFile.replace(".","_cartoon.")),cartoon)

# FOR ASCII
def acii(sourceFile):
    img = readImg(resolveFile(sourceFile))
    line_wdt =9
    blur_value = 7
    totalColor = 4
    grayFilter = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pywhatkit.image_to_ascii_art(sourceFile,'sample')

# FOR OIL PAINT
def paint(sourceFile):
    img = readImg(resolveFile(sourceFile))
    line_wdt =9
    blur_value = 7
    totalColor = 4
    grayFilter = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_resized = cv2.resize(img, None, fx=0.5, fy=0.5)

    image_cleared = cv2.medianBlur(image_resized, 1)
    image_cleared = cv2.medianBlur(image_cleared, 1)
    image_cleared = cv2.medianBlur(image_cleared, 1)

    image_cleared = cv2.edgePreservingFilter(image_cleared, sigma_s=20,sigma_r=0.15)

    image_filtered = cv2.bilateralFilter(image_cleared, 3, 10, 5)

    for i in range(2):
        image_filtered = cv2.bilateralFilter(image_filtered, 3, 20, 10)

    for i in range(3):
        image_filtered = cv2.bilateralFilter(image_filtered, 5, 30, 10)
    
    gaussian_mask= cv2.GaussianBlur(image_filtered, (7,7), 2)
    image_sharp = cv2.addWeighted(image_filtered, 1.5, gaussian_mask, -0.5, 0)
    image_sharp = cv2.addWeighted(image_sharp, 1.4, gaussian_mask, -0.2, 10)

    cv2.imwrite(resolveFile(sourceFile.replace(".","_oil.")), image_sharp)
