from django.shortcuts import render
from django.http import HttpResponse


def datashow(request):
    if(request.method == 'GET'):
        serialnumber = '0645'
        selectedevice =  Device.objects.get(deviceserial = serialnumber)
        devicedata = Data.objects.filter(device = selectedevice).order_by("-pk")
        context = {'devicedata': devicedata}
        return render(request, 'tableview.html', context)
