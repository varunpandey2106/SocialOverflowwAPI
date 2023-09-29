from django.urls import path
from .import views

app_name='discussion'

urlpatterns = [
    
    path('',views.discussions,name='discussions'),
    path('create/',views.create_discussion,name='create-discussion'),
    path('vote/',views.update_vote,name='discussion-vote'),

]
