from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from .models import BlogPost, Like, Comment
from .forms import CommentForm

 


# Home Page - List of published posts
def home(request):
    if request.user.is_authenticated:
        posts = BlogPost.objects.all()
    else:
        posts = BlogPost.objects.filter(status=True).order_by('-published_date')
    return render(request, 'blog/home.html', {'posts': posts})

# Post Detail Page - Full post view
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post  # Associate the comment with the current post
            new_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
        
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

# Create Post Page
@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})

# Edit Post Page
@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form})

# Delete Post Page
@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/delete_post.html', {'post': post})

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'blog/register.html', {'form': form})

def like_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Check if the user has already liked the post (if using the Like model)
    if request.user.is_authenticated:
        # Check if the user has already liked this post
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:  # If it's a new like, increase the like count
            post.likes += 1
            post.save()

    return redirect('post_detail', pk=post.pk)