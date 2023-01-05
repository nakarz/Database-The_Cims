from django.urls import path
from .views import *

urlpatterns = [
    path('list/', fetch_all_level),
    path('delete/<old_level>', delete_level),
    path('update/<old_level>', update_page),
    path('update_new_xp/<old_level>', update_xp),
    path('create/', create_page),
    path('create_new_level/', create_new_level),
]
