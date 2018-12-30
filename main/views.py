from django.shortcuts import render
from django.views.generic import View
from .forms import UploadFileForm
from django.http import HttpResponse
from . import gridExtraction 

# Create your views here.
class CharacterExtractor(View):
    def get(self, request):
        return render(request, template_name="image_upload.html")

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        with open('uploads/image.png', 'wb+') as destination:
            for chunk in request.FILES['imagename']:
                destination.write(chunk)
        
        headerdict, resultlist = gridExtraction.imageCharacterExtracter('uploads/image.png')              
        #resultlist = [{"name": "Kabwama Alvin", "number": 999, "location": "Novia"}]
        return render(request, template_name="data_view.html", context={"resultlist": resultlist, 'headerdict': headerdict})
        # else:
        #     return HttpResponse("Not so good!")
