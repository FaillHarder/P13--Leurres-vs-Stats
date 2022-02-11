from django.urls import path
from app.usermanager import views

urlpatterns = [
    path('registrer', views.create_user, name='registrer')
]
