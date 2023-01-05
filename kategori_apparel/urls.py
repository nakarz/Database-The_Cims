from django.urls import path
from kategori_apparel.views import *

urlpatterns = [
    path('list/', fetch_kategori_apparel),
    path('create/', create_new_kategori_apparel),
    path('delete/<nama_kat_apparel>', delete_kategori_apparel),
]