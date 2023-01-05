from django.urls import path
from .views import *

urlpatterns = [
    path('list/', tampilkan_bekerja),
    path('start_bekerja/', start_work),
    path('create/<nama_tokoh>/<pekerjaan>/<base_honor>', create_bekerja),
]
