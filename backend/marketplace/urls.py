from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.get_csrf, name='csrf'),  # ← new
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('apps/', views.user_apps, name='user_apps'),  # ← ADD THIS
      path('logout/', views.logout_view, name='logout'), 
       path('public-apps/', views.public_apps, name='public_apps'),
]