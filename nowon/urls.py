"""
URL configuration for nowon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from nowonfeed import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('nowonfeed/', views.nowonfeed_view, name='nowonfeed'),
    path('toggle-like/', views.toggle_like_view, name='toggle-like'),
    path('commentary/', views.comentary, name='commentary'),
    path('comments/', views.comentaries_view, name='comments'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path("update_server/", views.update, name="update"),


    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),



    path('like/<int:post_id>/', views.like_post, name='like_post'),
]