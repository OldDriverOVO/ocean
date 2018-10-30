from django.urls import path
from . import views

app_name = 'partsinfo'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('part_list/', views.parts_list, name='part_list'),
    path('add_parts_info/', views.add_parts_info, name='add_parts_info'),
    path('factory_list/', views.factory_list, name='factory_list'),
    path('add_factory_info/', views.add_factory_info, name='add_factory_info'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('add_customer_info/', views.add_customer_info, name='add_customer_info'),
    path('factory_price_list/', views.factory_price_list, name='factory_price_list'),
    path('delete_factory_price/', views.delete_factory_price, name='delete_factory_price'),
    path('update_factory_price/', views.update_factory_price, name='update_factory_price'),
    path('part_detail/<pk>/', views.part_detail, name='part_detail'),
    path('customer_price_list/', views.customer_price_list, name='customer_price_list'),
    path('delete_customer_price/', views.delete_customer_price, name='delete_customer_price'),
    path('update_customer_price/', views.update_customer_price, name='update_customer_price'),
    path('add_factory_price/', views.add_factory_price, name='add_factory_price'),
    path('add_customer_price/', views.add_customer_price, name='add_customer_price'),
    path('factory_detail/<pk>/', views.factory_detail, name='factory_detail'),
]
