from django.urls import path

from app.fishingstats import views

urlpatterns = [
    path('stats/', views.stats, name="stats")
]
