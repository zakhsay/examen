from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from .validators import validate_css_js_url

class UserThemePreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    theme = models.ForeignKey('AdminTheme', on_delete=models.SET_NULL, null=True)

class AdminTheme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    css_url = models.CharField(max_length=255) # Changed to CharField
    js_url = models.CharField(max_length=255)  # Changed to CharField
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def save(self, *args, **kwargs):
        if self.is_active:
            # Ensure only one theme is active at a time
            AdminTheme.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def validate_css_js_url(value):
    if not (value.endswith('.css') or value.endswith('.js')):
        raise ValidationError('URL must end with .css or .js')

