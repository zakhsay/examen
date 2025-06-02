import requests
from celery import shared_task
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from .models import AdminTheme

@shared_task()
def validate_theme_urls(theme_id):
    try:
        theme = AdminTheme.objects.get(id=theme_id)
    except AdminTheme.DoesNotExist:
        return

    base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000') # Default to localhost for development

    if theme.css_url:
        try:
            if theme.css_url.startswith('http://') or theme.css_url.startswith('https://'):
                # If it's an absolute URL, use it directly
                final_css_url = theme.css_url
            else:
                # If it's a relative static URL, construct the absolute path
                final_css_url = f"{base_url}{staticfiles_storage.url(theme.css_url.lstrip('/'))}"

            response = requests.head(final_css_url, timeout=5)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            if 'text/css' not in response.headers.get('Content-Type', ''):
                raise ValueError(f"Invalid CSS Content-Type for {theme.css_url}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Invalid CSS URL: {theme.css_url} - {e}")
        except ValueError as e:
            raise e

    if theme.js_url:
        try:
            if theme.js_url.startswith('http://') or theme.js_url.startswith('https://'):
                # If it's an absolute URL, use it directly
                final_js_url = theme.js_url
            else:
                # If it's a relative static URL, construct the absolute path
                final_js_url = f"{base_url}{staticfiles_storage.url(theme.js_url.lstrip('/'))}"

            response = requests.head(final_js_url, timeout=5)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            if 'application/javascript' not in response.headers.get('Content-Type', '') and \
               'text/javascript' not in response.headers.get('Content-Type', '') and \
               'application/x-javascript' not in response.headers.get('Content-Type', ''):
                raise ValueError(f"Invalid JS Content-Type for {theme.js_url}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Invalid JS URL: {theme.js_url} - {e}")
        except ValueError as e:
            raise e

    # If validation passes, you might want to mark the theme as valid or perform other actions
    # For now, we just let it pass if no exceptions are raised.