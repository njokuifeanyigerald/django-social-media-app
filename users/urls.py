from django.urls import path
from django.urls import path
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
     path('', users_list, name='users_list'),
     path('<slug>/', profile_view, name='profile_view'),
     path('friend_request/send/<int:id>', send_friend_request, name='send_friend_request'),
     path('friend_request/cancel/<int:id>',cancel_friend_request, name="cancel_friend_request" ),
     path('friend_request/accept/<int:id>',accept_friend_request, name='accept_friend_request'),
     path('friend_request/delete/<int:id>', delete_friend_request, name='delete_friend_request'),
     path('friend/delete/<int:id>',delete_friend, name='delete_friend'),
     path('friends/',friend_list, name='friend_list'),
     path('edit_profile/', edit_profile, name='edit_profile' ),
     path('my_profile', my_profile, name='my_profile'),
    
]
