from django.http import HttpResponse
from django.views.generic.base import View

class ExceptView(View):
    
    def get(self, request):
        raise ValueError

class IndexView(View):

    def get(self, request):
        return HttpResponse("This is the index view!")
    