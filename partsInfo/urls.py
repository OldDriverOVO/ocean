
from django.urls import path
from . import views


app_name='partsinfo'
urlpatterns = [
    path('', views.index,name='index'),
    path('part_list/', views.parts_list,name='part_list'),

]