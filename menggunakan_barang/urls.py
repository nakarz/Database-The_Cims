from django.urls import path
from .views import *

urlpatterns = [
    path('list/', tampilkan_using_item),
    path('create/', create_using_item),
    path('create_new_use_item/', create_new_use_item),
]
