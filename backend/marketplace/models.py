from django.db import models

class AIApp(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    launch_url = models.URLField()
    price_tier = models.CharField(
        max_length=20,  # ← increased from 10 to 20
        choices=[
            ('free', 'Free'),
            ('paid', 'Paid'),
            ('coming_soon', 'Coming Soon')
        ],
        default='free'
    )
    category = models.CharField(max_length=50, default='General')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title