from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Create your views here.
class Urinalysis(View):
    def get(self, request):
        return render(request, template_name="data_input.html")

    def post(self, request):
        print(request.POST.get("nitritesID"))
        return "hello"
        