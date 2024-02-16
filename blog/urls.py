
from django.contrib import admin
from django.urls import path
from .views import register, profile, PostListView, detail, PostCreateView, \
    PostUpdateView, \
    PostDelete, \
    like_post, post_comment, profile_list_view, \
    SearchUser, profile_detail, user_post, share_post, posts_of_following_profile

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',PostListView.as_view(),name='index'),
    path('shared_post/<int:pk>/',share_post,name='shared_post'),
    path('profile_list/',profile_list_view,name='profiles_list'),
    path('like/',like_post,name='like'),
    path('comment/', post_comment, name='comment'),
    path('detail/<int:pk>/',detail,name='detail'),
    path('detail/<int:pk>/update/',PostUpdateView.as_view(),name='update'),
    path('detail/<int:pk>/delete/',PostDelete.as_view(),name='delete'),
    path('create/',PostCreateView.as_view(),name='create'),
    path('register/',register,name='register'),
    path('profile/',profile,name='profile'),
    path('user_post/',user_post,name='user_post'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('search/',SearchUser.as_view(), name='search'),
    path('search_profile/<int:pk>/', profile_detail, name='search_profile'),

    path('posts_of_following/', posts_of_following_profile, name='all_following_post'),


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
