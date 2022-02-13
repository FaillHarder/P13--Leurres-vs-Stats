from django.urls import path
from app.usermanager import views

urlpatterns = [
    path('registrer', views.create_user, name='registrer'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
]
