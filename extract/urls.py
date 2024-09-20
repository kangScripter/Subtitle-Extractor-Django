from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('video',views.VideoUpload,name="video"),
    path('query',views.Query,name='query'),
    path('list',views.List,name='list'),
    path('login',views.Login,name='login'),
    path('register',views.Register,name='register'),
    path('logout',views.Logout,name='logout'),
    path('player', views.PlayVideo, name='player')
]