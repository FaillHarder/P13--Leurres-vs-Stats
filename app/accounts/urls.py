from django.urls import path, include
from app.accounts import views

urlpatterns = [
    path('profile/', include([
        path('', views.profile, name="profile"),
        path('edit', views.edit_profile, name="edit_profile")
    ])),
    path('my_catch/', include([
        path('', views.my_catch, name="my_catch"),
        path('edit/<int:id>/', views.my_catch_edit, name="my_catch_edit"),
        path('delete/<int:id>/', views.my_catch_delete, name="my_catch_delete")
    ]))
]
