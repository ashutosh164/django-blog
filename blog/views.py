from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SharedForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.core.mail import send_mail
from django.views import View
from django.db.models import Q
from django.utils import timezone


class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'post'
    ordering = ['-date_created', '-shared_on']
    paginate_by = 2


def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()

    return redirect('index')


def detail(request, pk):
    object = Post.objects.get(id=pk)
    posts = get_object_or_404(Post, id=pk)
    post_liked = posts.liked.all()
    comments = posts.comments.filter()

    context = {
        'object': object,
        'post_liked':post_liked,
        'comments':comments
    }
    return render(request, 'detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'post_form.html'

    # This line of code brings the user who create the post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'post_form.html'

    # This line of code brings the user who create the post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # This function is check the user and permitted to access this function if the user is create this post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    # If the user is create this post can delete the post otherwise not permitted
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username}!")
            # subject = 'welcome world Blog app'
            subject = 'welcome to my social world'
            message = f'Hi {user.username}, thanks you'
            email_from = settings.EMAIL_HOST_USER
            recipent_list = [user.email, ]
            send_mail(subject, message, email_from, recipent_list)
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request,'register.html',{'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your Account has been updated!")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        post_count = Post.objects.filter(author=request.user).count()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'post_count': post_count
    }

    return render(request,'profile.html', context)


@login_required
def post_comment(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        body = request.POST.get('body')
        comment = Comment(user=user, post=post, body=body)
        comment.save()
        messages.success(request, 'you comment has been posted')
        return redirect('index')


@login_required
def profile_list_view(request):
    user = request.user
    qs = Profile.objects.all().exclude(user=user)

    context = {'qs':qs}

    return render(request, 'profile_list.html', context)


class SearchUser(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile = Profile.objects.filter(Q(user__username__istartswith=query))

        context = {'profile': profile}

        return render(request, 'search.html', context)


def profile_detail(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    return render(request, 'profile_detail.html', {'profile':profile})


def user_post(request):
    post = Post.objects.filter(author=request.user)

    context = {
        'post': post
    }
    return render(request, 'user_post.html', context)


def share_post(request, pk):
    post = Post.objects.get(id=pk)
    # post = get_object_or_404(Post, id=pk)
    form = SharedForm()

    if request.method == 'POST':
        original_post = Post.objects.get(id=pk)
        form = SharedForm(request.POST)

        if form.is_valid():
            new_post = Post(shared_title=request.POST.get('title'),
                            title=original_post.title,
                            author=original_post.author,
                            date_created=original_post.date_created,
                            shared_user=request.user,
                            shared_on=timezone.now())
            new_post.save()
            for img in original_post.image.all():
                new_post.image.add(img)
            new_post.save()
        return redirect('index')

    context = {'post': post,
               'form': form
               }
    return render(request, 'shared_form.html', context)