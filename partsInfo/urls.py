
from django.urls import path
from . import views


app_name='partsinfo'
urlpatterns = [
    path('', views.index,name='index'),
    path('part_list/', views.parts_list,name='part_list'),
    path('add_parts_info/', views.add_parts_info,name='add_parts_info'),
    path('factory_list/',views.factory_list,name='factory_list'),
    path('add_factory_info/',views.add_factory_info,name='add_factory_info'),
    path('customer_list/',views.customer_list,name='customer_list'),
    path('add_customer_info/',views.add_customer_info,name='add_customer_info'),

]