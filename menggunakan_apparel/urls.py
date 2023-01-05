from django.urls import path
from .views import *

urlpatterns = [
    path('list/', fetch_all_using_apparel),
    path('delete/<tokoh_name>/<id_koleksi>', delete_use_apparel),
    path('create/', create_page),
    path('get_id_apparel/', get_id_apparel),
    path('create_new_use_apparel/', create_new_use_apparel),
]
