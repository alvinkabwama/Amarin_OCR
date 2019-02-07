
import tesserocr
from PIL import Image
import cv2
import numpy as np


#IMAGEDISPLAYING
def image_show(header, image):
    '''
    cv2.imshow(header, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''


#PREPROCESSING THE IMAGE AND REMOVING THE NOISE 
def imagepreprocess(imageinput, checker):
    
    #LOADING THE IMAGE 
    header = 'Colourimage_image'
    image_show(header, imageinput)
    
    
    #GRAYSCALEIMAGE
    if checker is True:
        grayscale = cv2.cvtColor(imageinput, cv2.COLOR_RGB2GRAY)
        header = 'Grayscaleimage'
        image_show(header, grayscale)
    
    else:
        grayscale = imageinput
        image_show(header, grayscale)
        
    
    #BLURRING IMAGE 
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
    title = 'Blurred_image'
    image_show(title, blurred)
    

    #THRESHOLDING
    #ret,thresh1 = cv2.threshold(blurred,150,255,cv2.THRESH_BINARY)
    thresh1 = cv2.adaptiveThreshold(grayscale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 25)
    header = 'Thresholded_image'
    image_show(header, thresh1)
    img = thresh1
    
    
    #INVERTING COLORS
    img = thresh1
    img = cv2.bitwise_not(img, img)
    header = 'Inverted_image'
    image_show(header, img)
 
    
    
    #DILATING IMAGE
    if checker is True:
        kernel = np.ones((4,4),np.uint8)
    else:
        kernel = np.ones((3,3),np.uint8)
    imageinput = cv2.dilate(thresh1, kernel, iterations = 1)
    header = 'Dilated_image'
    image_show(header, img)
    
    
    #REINVERTING COLORS
    img = imageinput
    img = cv2.bitwise_not(img, img)
    header = 'Reinverted_image'
    image_show(header, img)
    
    #RESIZING THE IMAGE
    xscalefactor = 1.3
    yscalefactor = 1.3
    img = cv2.resize(img,None,fx=xscalefactor, fy=yscalefactor, interpolation = cv2.INTER_CUBIC)
    
    #SAVING TEMPORARY IMAGE
    cv2.imwrite('images/temp.png', img)
    

def tesserpredict(img, state):   
    if(state is True):       
        imagepreprocess(img, checker = True)
        tempimg = Image.open('images/temp.png')  
        text = tesserocr.image_to_text(tempimg)
    else:
        cv2.imwrite('images/temp.png', img)
        tempimg = Image.open('images/temp.png')  
        text = tesserocr.image_to_text(tempimg)
<<<<<<< HEAD
    #print(text)
=======
>>>>>>> 49076f1bd4ccc9ae745e0edde29d2a5e3e50fa65
    return text

'''
imagefile = 'images/image32.jpg'
imgin = cv2.imread(imagefile)
output = tesserpredict(imgin)
print(output)

tempimg = Image.open(imagefile)  
print(tesserocr.image_to_text(tempimg))
'''

