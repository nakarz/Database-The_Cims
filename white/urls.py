from django.urls import path
from .views import index, login_page, home_page, logout, register_admin, register_player, create_character, \
    character_list, character_detail, update_character

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_page),
    path('home/', home_page, name='home'),
    path('logout/', logout),
    path('register/', register_player),
    path('register-admin/', register_admin),
    path('character', character_list),
    path('character/create', create_character),
    path('character/detail', character_detail),
    path('character/update', update_character)
]
