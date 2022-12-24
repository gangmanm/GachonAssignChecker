
from django.urls import path, include
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('',views.home, name='home')
]
