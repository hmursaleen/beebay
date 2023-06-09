from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('like/<int:blog_id>/', views.like_blog, name='like_blog'),
    path('add_comment/<int:blog_id>/', views.add_comment, name='add_comment'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('send_message/<str:username>/', views.send_message, name='send_message'),
    path('message_thread/<str:username>/', views.message_thread, name='message_thread'),
    path('search_users/', views.search_users, name='search_users'),
]
