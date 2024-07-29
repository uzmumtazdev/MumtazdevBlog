from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<int:pk>/', views.detail, name='detail'),
    path('blog/add/', views.create_post, name='add')
]
