from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^view_raises_exception/', views.exception_view),
    url(r'^view_raises_no_exceptions/', views.no_exception_view),
]
