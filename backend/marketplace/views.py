from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
import json

@ensure_csrf_cookie  # ← This sets the CSRF cookie on GET requests
def get_csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username taken'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return JsonResponse({'message': 'Registered and logged in', 'user': username})
    return JsonResponse({'error': 'POST only'}, status=405)

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Logged in', 'user': username})
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse({'error': 'POST only'}, status=405)

def user_profile(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'username': request.user.username,
            'email': request.user.email,
        })
    return JsonResponse({'error': 'Not authenticated'}, status=401)

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import AIApp

@login_required
def user_apps(request):
    """Return apps the user has access to (free for all, paid for specific users)."""
    # Get all active free apps
    apps = list(AIApp.objects.filter(is_active=True, price_tier='free').values())

    # Add paid apps if user is authorized
    # TODO: In Phase 4, check real subscriptions
    if request.user.username in ['admin', 'jude_user', 'fadipe']:  # ← add your username
        paid_apps = AIApp.objects.filter(is_active=True, price_tier='paid').values()
        apps.extend(list(paid_apps))

    return JsonResponse({"apps": apps})
from django.contrib.auth import logout as django_logout

def logout_view(request):
    """Log user out and destroy session."""
    django_logout(request)
    return JsonResponse({'message': 'Logged out successfully'})
def public_apps(request):
    """Public endpoint: returns all active apps (safe for catalog)."""
    apps = AIApp.objects.filter(is_active=True).values(
        'id', 'title', 'description', 'price_tier', 'category'
    )
    # Map price_tier to user-friendly labels
    app_list = []
    for app in apps:
        price_label = {
            'free': 'Free',
            'paid': 'Paid',
            'coming_soon': 'Coming Soon'
        }.get(app['price_tier'], app['price_tier'])
        
        app_list.append({
            'id': app['id'],
            'title': app['title'],
            'description': app['description'],
            'price': price_label,
            'category': app['category']
        })
    
    return JsonResponse({'apps': app_list})