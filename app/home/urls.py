from django.urls import path
from app.home import views

urlpatterns = [
    path('', views.index, name='index')
]
