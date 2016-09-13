from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^exception$', views.ExceptView.as_view()) #, name="except_view"
    ]
