from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),
    path("", include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    
    #path("nameform/", views.nameForm, name="nameform")
]