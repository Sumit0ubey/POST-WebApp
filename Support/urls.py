from django.urls import path
from Support.views import contact

urlpatterns = [
    path('', contact, name='Contact'),
]
