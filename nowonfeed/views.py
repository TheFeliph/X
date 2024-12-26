# views.py
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, render
from django import forms
from django.http import JsonResponse
from django.core.management import call_command
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import git


from .forms import CustomUserCreationForm  

def run_migrations():
    call_command('migrate')

run_migrations()

User = get_user_model()

if not User.objects.filter(username='user').exists():
    User.objects.create_user(username='user', password='user')

class PostForm(forms.Form):
    content = forms.CharField(max_length=280)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('nowonfeed')  
        else:
            return render(request, 'nowonfeed/login.html', {'error': 'Credenciais inválidas'})

    return render(request, 'nowonfeed/login.html')

def register_view(request):
    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('login')  
    else:
        form = CustomUserCreationForm() 
    return render(request, 'nowonfeed/register.html', {'form': form})

@csrf_exempt
def nowonfeed_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    form = PostForm()
    posts = request.session.get('posts', [])

    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            content = request.POST.get('content')
            if content:
                posts.insert(0, content)
                request.session['posts'] = posts
                return JsonResponse({'new_post': content, 'username': request.user.username})
            else:
                return JsonResponse({'error': 'Invalid content'}, status=400)

        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.cleaned_data['content']
            posts.insert(0, new_post)
            request.session['posts'] = posts

    return render(request, 'nowonfeed/feed.html', {'form': form, 'posts': posts})

def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def update(request):
    if request.method == "POST":
        repo = git.Repo('/home/feliph2004/nowon')
        origin = repo.remotes.origin
        origin.pull()
        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")








from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Like

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_detail', post_id=post.id)


from django.shortcuts import render, get_object_or_404
from .models import Post  # Substitua `Post` pelo modelo correto do seu projeto

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})




from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Post, Like

def toggle_like(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            return JsonResponse({'status': 'unliked', 'likes_count': post.likes.count()})
        return JsonResponse({'status': 'liked', 'likes_count': post.likes.count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)





from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Post

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})

