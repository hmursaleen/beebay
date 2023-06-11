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
    #path('edit_profile/', views.edit_profile, name='edit_profile'),
]
