from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AdminTheme
from .tasks import validate_theme_urls

@receiver(post_save, sender=AdminTheme)
def theme_post_save(sender, instance, created, **kwargs):
    validate_theme_urls.delay(instance.id)