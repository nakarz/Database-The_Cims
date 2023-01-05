from django.urls import path
from koleksi.views import *

urlpatterns = [
    path('create/', create_koleksi),
    # CREATE FORM
    path('form/form_rambut/', create_koleksi_rambut),
    path('form/form_mata/', create_koleksi_mata),
    path('form/form_barang/', create_koleksi_barang),
    path('form/form_rumah/', create_koleksi_rumah),
    path('form/form_apparel/', create_koleksi_apparel),
    # CREATE POST
    path('create_new_koleksi_rambut/', create_new_koleksi_rambut),
    path('create_new_koleksi_mata/', create_new_koleksi_mata),
    path('create_new_koleksi_barang/', create_new_koleksi_barang),
    path('create_new_koleksi_rumah/', create_new_koleksi_rumah),
    path('create_new_koleksi_apparel/', create_new_koleksi_rambut),
    # LIST
    path('list/', fetch_koleksi),
    path('list/list_apparel/', fetch_koleksi_list_apparel),
    path('list/list_rambut/', fetch_koleksi_list_rambut),
    path('list/list_barang/', fetch_koleksi_list_barang),
    path('list/list_mata/', fetch_koleksi_list_mata),
    path('list/list_rumah/', fetch_koleksi_list_rumah),
    #UPDATE
    path('update/<koleksi>', update_koleksi),
    path('delete/<koleksi>', delete_koleksi),
    path('update_rambut_admin/<str:id>/<str:harga>/<str:tipe>',update_rambut_admin,name='update_rambut_admin'),
    path('update_mata_admin/<str:id>/<str:harga>/<str:warna>',update_mata_admin,name='update_mata_admin'),
    path('update_rumah_admin/<str:id>/<str:nama>/<str:harga>/<str:harga_beli>/<str:kapasitas_barang>', update_rumah_admin,name='update_rumah_admin'),
    path('update_barang_admin/<str:id>/<str:nama>/<str:harga>/<str:harga_beli>/<str:tingkat_energi>',update_barang_admin,name='update_barang_admin'),
    path('delete_rambut_admin/<str:pk>', delete_rambut_admin, name='delete_rambut_admin'),
    path('delete_mata_admin/<str:pk>', delete_mata_admin, name='delete_mata_admin'),
    path('delete_rumah_admin/<str:pk>', delete_rumah_admin, name='delete_rumah_admin'),
    path('delete_barang_admin/<str:pk>', delete_barang_admin, name='delete_barang_admin'),

]
