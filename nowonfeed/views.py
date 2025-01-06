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
import random
import string


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
    allPosts = request.session.get('posts', [])
    primarysPosts = [post for post in allPosts if post.get("isPrimary")] 
    post_id_counter = request.session.get('post_id_counter', 1)

    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            content = request.POST.get('content')
            if content:
                # Gerar ID de 5 dígitos usando o contador
                post_id = str(post_id_counter).zfill(5)  # Preenche com zeros à esquerda até ter 5 caracteres

                post_object = {"id": post_id, "post": content, "isLiked": False, "isPrimary": True}
                allPosts.insert(0, post_object)
                request.session['posts'] = allPosts
                request.session['post_id_counter'] = post_id_counter + 1  # Incrementa o contador para o próximo ID
                return JsonResponse({'new_post': post_object, 'username': request.user.username})
            else:
                return JsonResponse({'error': 'Invalid content'}, status=400)

        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.cleaned_data['content']

            # Gerar ID de 5 dígitos usando o contador
            post_id = str(post_id_counter).zfill(5)  # Preenche com zeros à esquerda até ter 5 caracteres

            post_object = {"id": post_id, "post": new_post, "isLiked": False, "isPrimary": True}
            primarysPosts.insert(0, post_object)
            request.session['posts'] = primarysPosts
            request.session['post_id_counter'] = post_id_counter + 1  # Incrementa o contador para o próximo ID

    return render(request, 'nowonfeed/feed.html', {'form': form, 'posts': primarysPosts})

def comentaries_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    param_value = request.GET.get('param', None)  # 'param' é o nome do parâmetro na URL
    allPosts = request.session.get('posts', [])
    main_post = next((post for post in allPosts if post.get("id") == param_value), None)
    filtered_posts = [post for post in allPosts if post['id'][-5:] == param_value[:5] and not post['isPrimary']]
    # post_id_counter = request.session.get('post_id_counter', 1)
    
    return render(request, 'nowonfeed/comentaries.html', {'param_value': param_value, 'main_post': main_post, 'posts': filtered_posts})


@csrf_exempt
def toggle_like_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    tweet_id = request.GET.get('id')

    posts = request.session.get('posts', [])

    for post in posts:
        if post.get('id') == tweet_id:  
            post['isLiked'] = not post['isLiked']  
            break
    else:
        return JsonResponse({'error': 'Tweet não encontrado'}, status=404)

    request.session['posts'] = posts

    tweet = next(post for post in posts if post['id'] == tweet_id)
    return JsonResponse({
        'success': True,
        'id': tweet_id,
        'isLiked': tweet['isLiked']  
    })
    

@csrf_exempt
def comentary(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = PostForm()

    tweet_id = request.GET.get('id')

    posts = request.session.get('posts', [])
    post_id_counter = request.session.get('post_id_counter', 1)


    new_post = request.POST.get('content')

    # Gerar 5 caracteres aleatórios (letras e números)
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    first_five_chars = tweet_id[:5]

    
    # Concatenar com o tweet_id
    post_id = f"{random_suffix}{first_five_chars}"

    post_object = {"id": post_id, "post": new_post, "isLiked": False, "isPrimary": False}
    posts.insert(0, post_object)
    request.session['posts'] = posts
    request.session['post_id_counter'] = post_id_counter + 1

    return JsonResponse({'param_value': tweet_id})

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

