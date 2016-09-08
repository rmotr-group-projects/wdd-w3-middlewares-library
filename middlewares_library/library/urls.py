from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test', views.TestView.as_view()),
    url(r'^exception', views.ExceptionView.as_view())
]
