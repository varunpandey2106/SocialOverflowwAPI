from django.urls import path
from .import views

app_name='feed'

urlpatterns = [
    path('', views.feed_posts, name="feed-posts"),
    path('create/', views.create_feedpost, name="feedpost-create"),
    path('edit/<str:pk>/', views.edit_feedpost, name="feedpost-edit"),
    path('details/<str:pk>/', views.feedpost_details, name="feedpost-details"),
    path('reshare/', views.reshare, name="feedpost-reshare"),
    path('vote/', views.update_vote, name="feedpost-vote"),
    path('delete/<str:pk>/', views.delete_feedpost, name="delete-feedpost"),
    path('<str:pk>/comments/', views.feedpost_comments, name="feedpost-comments"),

]