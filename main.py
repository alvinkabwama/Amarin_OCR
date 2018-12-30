import requests
from . import gridExtraction
import imghdr
import time

request_url = "http://18.191.62.27/api/request"
download_delay = 15
resp = requests.get(request_url).json()

status = resp.get("status")
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

        headerdict, resultlist = gridExtraction.imageCharacterExtracter('uploads/image.png')

        send_data = {'resultList': resultlist,
                     'headerDict': headerdict,
                     'id': image_id}
        requests.post(request_url, data=send_data)

elif status == 204:
    pass

else:
    pass
