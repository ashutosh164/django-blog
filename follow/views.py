from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from blog.models import Profile
from django.contrib import messages
from django.http import HttpResponseRedirect


def follow_unfollow_profile(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)
        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
            messages.warning(request, f'Hi! {request.user},Now You are Unfollowing {obj.user}')
        else:
            my_profile.following.add(obj.user)
            messages.success(request, f'Hi {request.user}, Now You are following {obj.user}')
        # return redirect(request.method.META.get('HTTP_REFERER'))
        # return redirect('profiles:profile_detail')
        # return HttpResponseRedirect('')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:profile_list')


class ProfileListView(ListView):
    model = Profile
    template_name = 'profile/main.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile/detail.html'

    # def get_object(self, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     print(pk)
    #     view_profile = Profile.objects.get(pk=pk)
    #     print(view_profile)
    #     return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False
        context['follow'] = follow
        return context











