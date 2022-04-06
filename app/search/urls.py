from django.urls import path
from app.search import views

urlpatterns = [
    path('search', views.search, name="search")
]
