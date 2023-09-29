from django.urls import path
from .import views

app_name='feed'

urlpatterns = [
    path('', views.feed_posts, name="feed-posts"),
    path('create/', views.create_feedpost, name="feedpost-create"),
]