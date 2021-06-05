from django import http
from django.contrib.messages.api import success
from django.db.models.signals import post_save
from django.shortcuts import render,redirect, get_object_or_404
from .models import Profile, FriendRequest
# from feed.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login
from django.conf import settings
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
import random

User = get_user_model()

@login_required
def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_request = FriendRequest.objects.filter(from_user = request.user)
    sent_to = []
    friends = []
    for user in users:
        friend = user.friends.all()
        for f in friend:
            if f in friend:
                friend = friend.exclude(user=f.user)
        friends+=friend
    my_friends = request.user.profile.friends.all()
    for i in my_friends:
        if i in friends:
            friend.remove(i)
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in friends:
            random_list.remove(r)
    friends+=random_list
    for i in my_friends:
        if i in friends:
            friend.remove(i)
    for se in sent_friend_request:
        sent_to.append(se.to_user)
    context = {
        'users': friends,
        'sent': sent_to
    }
    return render(request, 'users/users_list.html')


def friend_list(request):
    p = request.user.profile
    friends =  p.friends.all()
    context = {
        'friends': friends
    }
    return render(request, 'users/friend_list.html', context)

@login_required
def send_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FriendRequest.objects.get_or_create(
        from_user  = request.user,
        to_user = user
    )
    # return HttpResponseRedirect('/users/{}'.format(user.profile.slug))
    # my method 
    return HttpResponseRedirect(f'/users/{user.profile.slug}')

@login_required
def cancel_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FriendRequest.objects.get_or_create(
        from_user  = request.user,
        to_user = user
    ).first()
    frequest.delete()
    return HttpResponseRedirect(f'/users/{user.profile.slug}')

@login_required
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.request.user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    if(FriendRequest.objects.filter(from_user=request.user, to_user = from_user).first()):
        request_rev = FriendRequest.objects.filter(from_user=request.user, to_user = from_user).first()
        request_rev.delete()
    frequest.delete()
    return HttpResponseRedirect(f'/users/{request.user.profile.slug}')

@login_required
def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user)
    frequest.delete()
    return HttpResponseRedirect(f'/users/{request.user.profile.slug}')

def delete_friend(request, id):
    user_profile  = request.user.profile
    friend_profile = get_object_or_404(Profile, id=id)
    user_profile.friends.remove(friend_profile)
    friend_profile.friends.remove(user_profile)
    return HttpResponseRedirect(f'/users/{friend_profile.slug}')

@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    u = p.user
    send_friend_request = FriendRequest.objects.filter(from_user=p.user)
    rec_friend_request  = FriendRequest.objects.filter(to_user=p.user)
    # user_posts = Post.objects.filter(user_name=u)
    friends = p.friends.all()

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not friend'

        # if we have sent him/her a friend request
        if len(FriendRequest.objects.filter(
            from_user=request.user).filter(to_user=p.user)) ==1:
            button_status = 'friend request sent'

        # if we have received a friend request
        if len(FriendRequest.objects.filter(from_user=p.user).filter(to_user=request.user)):
            button_status = 'friend request received'
    
    context = {
        'u': u,
        'button_status': button_status,
        'friend_list': friends,
        'send_friend_request': send_friend_request,
        'rec_friend_request': rec_friend_request,
        # 'post_count': users_posts.count
    }
    return render(request, 'user/profile.html', context)

def register(request):
    # used my own style
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages,success(request,  f'your account has been created! you can login')
            return redirect('login')
    context = {
        'form':form
    }
    return render(request, 'user/register.html', context)

@login_required
def edit_profile(request):
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,  request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('my_profile')
    # used my own style
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/edit_profile.html',context)
       
@login_required
def my_profile(request):
    p = request.user.profile
    you = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=you)
    rec_friend_requests = FriendRequest.objects.filter(to_user = you)
    # user_posts = Post.objects.filter(username=you)
    friends = p.friends.all()

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status= 'not friend'

        # if we have sent him/her a friend request
        if len(FriendRequest.objects.filter(from_user=request.user)
        .filter(to_user=you)) ==1:
            button_status = 'friend request sent'

        # if he/she sent a friend request

        if len(FriendRequest.objects.filter(from_user=you)
        .filter(to_user=you)) ==1:
            button_status =  'friend request received'
        
    context = {
        'u': you,
        'button_status':button_status,
        'friend_list':friends,
        'sent_friend_requests':sent_friend_requests,
        'rec_friend_requests':rec_friend_requests,
        # post_count: user_posts.count
    }
    return render(request, 'users/profile.html', context)

@login_required
def search_users(request):
    query = request.GET.get('q')
    object_list = User.objects.filter(username__icontains=query)
    context = {
        'users': object_list
    }
    return render(request, 'users/search.html', context)
