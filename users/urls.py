from django.urls import path
from django.urls.conf import include
from .views import users_list

urlpatterns = [
     path('', users_list, name='users_list'),
]
