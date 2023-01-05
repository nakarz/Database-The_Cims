from django.urls import path
from .views import *

urlpatterns = [
    path('list/', tampilan_job),
    path('create/', create_job),
    path('create_new_job/', create_new_job),
    path('delete/<old_job>', delete_job),
    path('update/<old_job>', update_job),
    path('update_new_base_honor/<old_job>', update_base_honor),
]
