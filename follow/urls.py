from django.contrib import admin
from django.urls import path
from .views import follow_unfollow_profile, ProfileListView, ProfileDetailView

urlpatterns = [
    path('follow_request/', follow_unfollow_profile, name='follow_request'),
    # path('all_profile/', ProfileListView.as_view(), name='profiles_list'),
    path('switch_follow/', follow_unfollow_profile, name='follow_unfollow_view'),
    path('<pk>/', ProfileDetailView.as_view(), name='profile_detail'),
]


