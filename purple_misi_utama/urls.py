from django.urls import path
from purple_misi_utama.views import main_mission, mission_detail, do_mission, create_main_mission, \
    create_do_main_mission, update_do_main_mission, delete_main_mission

urlpatterns = [
    path('', main_mission),
    path('detail/<str:mission_name>', mission_detail),
    path('create', create_main_mission),
    path('delete', delete_main_mission),
    path('do-mission', do_mission),
    path('do-mission/create', create_do_main_mission),
    path('do-mission/update', update_do_main_mission)
]
