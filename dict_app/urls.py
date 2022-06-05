from os import name
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home , name='home'),
    path('translate/', views.translate, name='translate'),
    path('recommand/', views.recommand, name='recommand'),
]
