from django.urls import path
from .views import food_list, eat_list, create_food, update_food, create_eat, delete_food

urlpatterns = [
    path('', food_list),
    path('create/', create_food),
    path('update/', update_food),
    path('delete/', delete_food),
    path('eat/', eat_list),
    path('eat/create', create_eat)
]
