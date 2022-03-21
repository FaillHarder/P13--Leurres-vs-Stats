from django.urls import path
from app.adddata import views

urlpatterns = [
    path('catchfish', views.catchfish, name="catchfish")
]
