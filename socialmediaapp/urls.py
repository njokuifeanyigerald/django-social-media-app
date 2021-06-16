from django.contrib import admin
from django.urls import path, include
from users.views import *
from django.contrib.auth import logout, views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('feed.urls')),
    path('users/', include('users.urls')),
    path('search/',search_users, name='search_users'),
    path('register/',register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name="users/login.html"), name='login' ),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name="users/password_rest.html"), name="password_reset"),
    path('password-reset/done',auth_views.PasswordResetView.as_view(template_name="users/password_rest_done.html"), name="password_reset_done"),
    path('password-reset-confirm',auth_views.PasswordResetConfirmView.as_view(template_name="users/password_rest_confirm.html"), name="password_reset_confirm"),
    path('password-reset-complete',auth_views.PasswordResetCompleteView.as_view(template_name="users/password_rest_complete.html"), name="password_reset_complete"),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
