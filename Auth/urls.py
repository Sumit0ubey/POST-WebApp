from django.urls import path

from Auth.views import signup, login, logout, profile

urlpatterns = [
    path('profile/', profile, name='Profile'),
    path('register/', signup, name='SignUp'),
    path('login/', login, name='Login'),
    path('logout/', logout, name='Logout')
]

