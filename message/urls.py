from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_messages, name="get-messages"),
    path('create-thread/', views.CreateThread,name="create-thread"),
    path('<str:pk>/read-message/', views.read_message, name="read-message"),
    path('create-message/', views.create_message, name="create-message"),
]