from django.http import HttpResponse
from django.views.generic.base import View


class TestView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        return HttpResponse()


class ExceptionView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        raise ValueError()
