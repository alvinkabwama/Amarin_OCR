import json
import requests
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from . import gridExtraction 

request_url = "http://18.191.62.27/api/request"

# Create your views here.
class CharacterExtractor(View):
    def get(self, request):
        return render(request, template_name="image_upload.html")

    def post(self, request):
        resp = requests.get(request_url).json()

        status = resp.get("status")
        if status == 200:
            image_id = resp.get("list").get("ID")
            image_url = resp.get("list").get("image")

            with open('uploads/image.png', 'wb+') as image_file:
                image_file.write(requests.get(image_url).content)

            headerdict, resultlist = gridExtraction.imageCharacterExtracter('uploads/image.png')

            send_data = {'resultList': resultlist,
                         'headerDict': headerdict,
                         'id': image_id}

            requests.post(request_url, data=send_data)

            # else:
            #     return HttpResponse("Not so good!")

        elif status == 204:
            pass

        else:
            pass
