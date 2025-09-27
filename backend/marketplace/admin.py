from django.contrib import admin
from .models import AIApp

@admin.register(AIApp)
class AIAppAdmin(admin.ModelAdmin):
    list_display = ['title', 'price_tier', 'category', 'is_active']
    list_filter = ['price_tier', 'category', 'is_active']
    search_fields = ['title']