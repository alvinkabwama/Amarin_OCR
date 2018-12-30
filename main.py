import requests
import gridExtraction
import imghdr
import time

prev_state = 0
download_delay = 5
request_url = "http://18.191.62.27/api/request"
polltime = 5


def acquirestatus():
    resp = requests.get(request_url).json()
    status = resp.get("status")
    print(status)
    return status, resp
    
    
def statusactive(status, resp):
    if status == 200:
        print("Pending data found! \n Processing....")
        image_id = resp.get("list").get("ID")
        image_url = resp.get("list").get("imageurl")
        image_name = resp.get("list").get("imagename")
        image_path = 'uploads/{}'.format(image_name)
    
        with open(image_path, 'wb+') as image_file:
            image_file.write(requests.get(image_url).content)
    
        time.sleep(download_delay)
    
        if imghdr.what(image_path) == "png" or imghdr.what(image_path) == "jpeg":
            print("Image file successfully downloaded!")
    
            headerdict, resultlist = gridExtraction.imageCharacterExtracter(image_path)
    
            send_data = {'resultList': resultlist,
                         'headerDict': headerdict,
                         'id': image_id}
            requests.post(request_url, data=send_data)
    
    elif status == 204:
        print(resp.get("message"))
        pass
       
    else:
        pass
    


while(True):
    print(prev_state)
    if prev_state is 1:
        print("Immediate_response")
    else:
        time.sleep(polltime)
        print("Delaying")
        
    liststatus, response = acquirestatus()
    statusactive(liststatus, response)
    
    if liststatus is 200:
        prev_state = 1
    elif liststatus is 204:
        prev_state = 0
    
    

