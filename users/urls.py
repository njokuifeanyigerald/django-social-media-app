from django.urls import path
from django.urls import path
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
     path('', users_list, name='users_list'),
     path('<slug>/', profile_view, name='profile_view'),
     path('friend_request/send/<int:id>', send_friend_request, name='send_friend_request'),
     path('friend',),
     path('',),
     path('', ),
     path('',),
     path('',),
     path('', ),
     path('',),
     path('',),
]
