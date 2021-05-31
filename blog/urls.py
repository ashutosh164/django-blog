"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import register,profile,PostListView,detail,PostCreateView,\
    PostUpdateView,\
    PostDelete,\
    like_post, post_comment, profile_list_view, SearchUser

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',PostListView.as_view(),name='index'),
    path('profile_list/',profile_list_view,name='profiles_list'),
    path('like/',like_post,name='like'),
    path('comment/', post_comment, name='comment'),
    path('detail/<int:pk>/',detail,name='detail'),
    path('detail/<int:pk>/update/',PostUpdateView.as_view(),name='update'),
    path('detail/<int:pk>/delete/',PostDelete.as_view(),name='delete'),
    path('create/',PostCreateView.as_view(),name='create'),
    path('register/',register,name='register'),
    path('profile/',profile,name='profile'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('search/',SearchUser.as_view(), name='search'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),


]
