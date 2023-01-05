from django.urls import path
from .views import *

urlpatterns = [
    path('list/', fetch_all_warna_kulit),
    path('delete/<wk_kode>', delete_warna_kulit),
    path('create/', create_page),
    path('create_new_warna_kulit/', create_new_warna_kulit),
]
