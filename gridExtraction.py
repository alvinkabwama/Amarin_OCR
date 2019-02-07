 # -*- coding: utf-8 -*-
import cv2
import numpy as np
import pandas as pd
import operator
import plotly.offline as py
py.init_notebook_mode(connected=True)
import tesserExtractionimport
import digitRecogimport
import re


total = 24.5
locratio1 = 4.85/total
locratio2 = 7.4/total
locratio3 = 4.7/total
locratio4 = 7.45/total


inforatio1 = 1.3/total
inforatio2 = 5.6/total
inforatio3 = 5.35/total
inforatio4 = 4.4/total
inforatio5 = 3.7/total
inforatio6 = 3.75/total



#DISPLAYING IMAGES 
def image_show(header, image):
    
    cv2.imshow(header, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    


#DISPLAYING THE CORNER POINTS ON THE IMAGE 
def display_points(header, in_img, points, radius=40, colour=(0, 0, 255)):
	"""Draws circular points on an image."""
	imgee = in_img.copy()

	# Dynamically change to a colour image if necessary
	if len(colour) == 3:
		if len(imgee.shape) == 2:
			imgee = cv2.cvtColor(imgee, cv2.COLOR_GRAY2BGR)
		elif imgee.shape[2] == 1:
			imgee = cv2.cvtColor(imgee, cv2.COLOR_GRAY2BGR)

	for point in points:
		imgee = cv2.circle(imgee, tuple(int(x) for x in point), radius, colour, -1)
	image_show(header, imgee)
    
   #CLEANING THE TEXT REMOVING THE WHITE SPACES AND FUNNY CHARACTERS 
def textclean(text):
    cleanedtext = re.sub('[^A-Za-z ]', '', text)
    print(cleanedtext)
    return cleanedtext

def numberclean(text):
    cleanedtext = re.sub('[^0-9]', '', text)
    print(cleanedtext)
    return cleanedtext
    



def imageCharacterExtracter(path):   
    #READ IMAGE AND CHANGE IT TO GRAY SCALE
    img = cv2.imread(path)
    baseimage = img
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    baseimagegrayscale = img
    
    
    #RESIZED IMAGE
    img = cv2.resize(img,None,fx=0.2, fy=0.2, interpolation = cv2.INTER_LINEAR)
    title = 'Resized_image'
    image_show(title, img)
    
    
    
    #APPLYING ADAPTIVE THRESHOLD
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 25)
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    title = 'Thresholded_image_image'
    image_show(title, img) 
    
    
    #INVERTING COLORS
    img = cv2.bitwise_not(img, img)
    title = 'Inverted_colours'
    image_show(title, img)
    contourimage = img
    
    
    #DILATE IMAGE TO RINCREASE SIZE OF GRID LINES
    kernel = np.ones((3,3),np.uint8)
    img = cv2.dilate(img, kernel, iterations = 1)
    title = 'Dilated_image'
    image_show(title, img)
    
    
    #FINDING CONTOURS TO ACQUIRE THE EDGE OF POLYGON
    new_img, ext_contours, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    new_img, contours, hier = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    # Draw all of the contours on the image in 2px red lines
    all_contours = cv2.drawContours(img.copy(), contours, -1, (0, 0, 255), 2)
    title = 'All-Contours'
    image_show(title, all_contours)
    
    
    external_only = cv2.drawContours(img.copy(), ext_contours, -1, (0, 0, 255), 2)
    title = 'External-Contours'
    image_show(title, external_only)
    
    #FINDING THE CORNERS OF THE BIGGEST CONTINUOUS POLYGON
    #_, contours, h = cv2.findContours(baseimagegrayscale, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
    im2, contours, hierarchy = cv2.findContours(baseimagegrayscale, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)  # Sort by area, descending
    polygon = contours[0]  # Largest image
    
    # Use of `operator.itemgetter` with `max` and `min` allows us to get the index of the point
    # Each point is an array of 1 coordinate, hence the [0] getter, then [0] or [1] used to get x and y respectively.
    
    # Bottom-right point has the largest (x + y) value
    # Top-left has point smallest (x + y) value
    # Bottom-left point has smallest (x - y) value
    # Top-right point has largest (x - y) value
    
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    
    # Return an array of all 4 points using the indices
    # Each point is in its own array of one coordinate
    corners = [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]
    
    title = 'Points'
    display_points(title, contourimage, corners)
    
    print('Top_Left', polygon[top_left][0])
    print('Top_Right', polygon[top_right][0])
    print('Bottom_Left', polygon[bottom_left][0])
    print('Bottom_Right', polygon[bottom_right][0])
    
    
    print('Bottom_Left', polygon[bottom_left][0][1])
    
    
    count = 0
    jsonlist = []
    threshold = 20
    ythreshold = 0
    
    #EXTRACTION OF INFORMATION ABOUT LOCATION AND VENUE 
    while count < 2:
        
        
        testimage = baseimage
        
        y_base = int(polygon[bottom_left][0][1]/11)
        y_cordinatefirst = count*y_base
        y_cordinatesecond = (count+1)*y_base
        
        x_cordinate0 = int(polygon[top_left][0][0])
        x_cordinate1 = int(polygon[top_right][0][0]*locratio1)
        x_cordinate2 = x_cordinate1 + int(polygon[top_right][0][0]*locratio2)
        x_cordinate3 = x_cordinate2 + int(polygon[top_right][0][0]*locratio3)
        x_cordinate4 = x_cordinate3 + int(polygon[top_right][0][0]*locratio4)
        
        if count == 0:   
            organisationimage = testimage[y_cordinatefirst+threshold:y_cordinatesecond-ythreshold, x_cordinate1+threshold:x_cordinate2-threshold]
            title = 'Organisation_name)'
            image_show(title, organisationimage)
            #first_name = characterExtractionimport.predictionwithfilter(crop_image1)
            organisation = tesserExtractionimport.tesserpredict(organisationimage, state = False)   
            organisation = textclean(organisation)
            
            
            activityimage = testimage[y_cordinatefirst+threshold:y_cordinatesecond-ythreshold, x_cordinate3+threshold:x_cordinate4-threshold]
            title = 'Activity_name'
            image_show(title, activityimage)
            #first_name = characterExtractionimport.predictionwithfilter(crop_image1)
            activity = tesserExtractionimport.tesserpredict(activityimage, state = True)
            activity = textclean(activity)
            
        if count == 1:   
            venueimage = testimage[y_cordinatefirst+threshold:y_cordinatesecond-ythreshold, x_cordinate1+threshold:x_cordinate2-threshold]
            title = 'Venue_name)'
            image_show(title, venueimage)
            #first_name = characterExtractionimport.predictionwithfilter(crop_image1)
            venue = tesserExtractionimport.tesserpredict(venueimage, state = False)
            venue = textclean(venue)
            
            
            
            dateimage = testimage[y_cordinatefirst+threshold:y_cordinatesecond-ythreshold, x_cordinate3+threshold:x_cordinate4-threshold]
            title = 'Date_name'
            image_show(title, dateimage)
            #first_name = characterExtractionimport.predictionwithfilter(crop_image1)
            date = tesserExtractionimport.tesserpredict(dateimage,  state = True)
            #date = textclean(date)
            
        count = count + 1
        
    headerdictionary = {
                        'organisation' : organisation,
                        'activity': activity,
                        'venue': venue,
                        'date': date,

            }
        
         
    
    
    #EXTRACTION OF THE INFORMATION
    jsonlist = []
    
    x_cordinate0 = int(polygon[top_left][0][0])
    x_cordinate1 = int(polygon[top_right][0][0]*inforatio1)
    x_cordinate2 = x_cordinate1 + int(polygon[top_right][0][0]*inforatio2)
    x_cordinate3 = x_cordinate2 + int(polygon[top_right][0][0]*inforatio3)   
    x_cordinate4 = x_cordinate3 + int(polygon[top_right][0][0]*inforatio4)
    x_cordinate5 = x_cordinate4 + int(polygon[top_right][0][0]*inforatio5)
    
    
    count = count + 1
    
    while count < 11:
        
        y_base = int(polygon[bottom_left][0][1]/11)
        y_cordinatefirst = count*y_base
        y_cordinatesecond = (count+1)*y_base
        
           
        #EXTRACTING THE FIRST NAME 
        fnameimage = testimage[y_cordinatefirst+threshold:y_cordinatesecond-ythreshold, x_cordinate1+threshold:x_cordinate2-threshold]
        title = 'Cropped_first_name'
        image_show(title, fnameimage)
        first_name = tesserExtractionimport.tesserpredict(fnameimage, state = True)
        first_name = textclean(first_name)
        
        
        #EXTRACTING THE SECOND NAME 
        snameimage = testimage[y_cordinatefirst+threshold:y_cordinatesecond-ythreshold, x_cordinate2+threshold:x_cordinate3-threshold]
        title = 'Cropped_second_name'
        image_show(title, snameimage)
        second_name = tesserExtractionimport.tesserpredict(snameimage, state = True)
        second_name = textclean(second_name)
        
    
        #EXTRACTING THE PHONE NUMBER
        numberimage = testimage[y_cordinatefirst+threshold:y_cordinatesecond-ythreshold, x_cordinate3+threshold:x_cordinate4-threshold]
        title = 'Cropped_phone_number'
        image_show(title, numberimage)
        cv2.imwrite('images/numbertemp.jpg', numberimage)
        numberfile = 'images/numbertemp.jpg'
        
        if(count is 3):
            number_model = digitRecogimport.train()
        number = digitRecogimport.predict(number_model, numberfile)       
        number = numberclean(number)
    
        #EXTRACTING THE LOCATION
        locationimage = testimage[y_cordinatefirst+threshold:y_cordinatesecond-ythreshold, x_cordinate4+threshold:x_cordinate5-threshold]
        title = 'Cropped_location'
        image_show(title, locationimage)
        location = tesserExtractionimport.tesserpredict(locationimage,state = True)
        location = textclean(location)
        count += 1
        
        monitordata = {
                        'name' : first_name + ' ' + second_name,
                        'phone' : number,
                        'location' : location,
                        }
        
        jsonlist.append(monitordata)
                  
    
    df = pd.DataFrame(jsonlist)
    
    df.to_csv('data.csv', index=True)
    
    return headerdictionary, jsonlist


#imageCharacterExtracter('images/py1.jpg')  

 


