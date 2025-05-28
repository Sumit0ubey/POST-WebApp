from django.urls import path

from Post.views import posts, post, createPost, updatePost, deletePost

urlpatterns = [
    path('', posts, name='Posts'),
    path('<int:id>', post, name='Post'),
    path('create/', createPost, name='createPost'),
    path('edit/<int:id>', updatePost, name='updatePost'),
    path('delete/<int:id>', deletePost, name='deletePost')
]
