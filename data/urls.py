
from django.urls import path

from .views import *

app_name = 'data'
urlpatterns = [
    path('items/',items_list,name='items_list_url'),
    path('demand/',demand_list,name='demand_list_url'),
    path('calculations/',calculations,name='calculations_url'),



    path('demand/create/',DemandCreate,name='demand_create_url'),
    path('item/create/',ItemCreate,name='item_create_url'),

    path('delete_items/<str:pk>/', delete_items, name="delete_items"),
    path('update_item/<str:pk>/',update_items,name="update_item"),


# path('view/',view,name="view"),




    


]
