from django.urls import path
from . import views

app_name = 'rank'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('rank/', views.rank, name='rank'),
]