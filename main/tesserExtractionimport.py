
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
    ret,thresh1 = cv2.threshold(blurred,140,255,cv2.THRESH_BINARY)
    header = 'Thresholded_image'
    image_show(header, thresh1)
    
    
    #INVERTING COLORS
    img = thresh1
    img = cv2.bitwise_not(img, img)
    header = 'Inverted_image'
    image_show(header, img)
 
    
    
    #DILATING IMAGE
    if checker is True:
        kernel = np.ones((2,2),np.uint8)
    else:
        kernel = np.ones((2,2),np.uint8)
    imageinput = cv2.dilate(thresh1, kernel, iterations = 1)
    header = 'Dilated_image'
    image_show(header, img)
    
    
    #REINVERTING COLORS
    img = imageinput
    img = cv2.bitwise_not(img, img)
    header = 'Reinverted_image'
    image_show(header, img)
    
    
    #SAVING TEMPORARY IMAGE
    cv2.imwrite('images/temp.png', img)
    

def tesserpredict(img):
    imagepreprocess(img, checker = True)
    tempimg = Image.open('images/temp.png')  
    text = tesserocr.image_to_text(tempimg)
    print(text)
    return text

'''
imagefile = 'images/image32.jpg'
imgin = cv2.imread(imagefile)
output = tesserpredict(imgin)
print(output)

tempimg = Image.open(imagefile)  
print(tesserocr.image_to_text(tempimg))
'''

