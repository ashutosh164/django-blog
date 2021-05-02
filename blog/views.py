from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'post'
    ordering = ['-date_created']


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
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username}!")
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
            messages.success(request,f"Your Account has been updated!")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form,
    }

    return render(request,'profile.html',context)


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

