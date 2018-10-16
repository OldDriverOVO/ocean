
from django.urls import path
from . import views


app_name='partsinfo'
urlpatterns = [
    path('', views.index,name='index'),
    path('parts/', views.parts,name='part_list'),

]