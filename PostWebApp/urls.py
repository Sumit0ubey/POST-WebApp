"""
URL configuration for PostWebApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

from Likes.views import root, like

urlpatterns = [
    path('', root, name='Home'),
    path('posts/', include('Post.urls')),
    path('auth/', include('Auth.urls')),
    path('likes/<int:id>', like, name='Like'),
    path('support', include('Support.urls')),
]
