from django.http import HttpResponse
from django.views.generic.base import View

# implement your views here
def exception_view(request):
    raise SyntaxError('Custom error message...')

def no_exception_view(request):
    return HttpResponse(200)