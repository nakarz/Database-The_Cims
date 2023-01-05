from django.urls import path
from koleksi_tokoh.views import *

urlpatterns = [
    path('list/', fetch_koleksi_tokoh),
    path('create/', create_koleksi_tokoh),
    path('create_new_koleksi_tokoh/', create_new_koleksi_tokoh),
    # path('get_id_koleksi/', get_id_koleksi_tokoh),
    path('delete/<tokoh>', delete_koleksi_tokoh)
]
