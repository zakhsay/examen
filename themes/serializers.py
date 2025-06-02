from rest_framework import serializers
from .models import AdminTheme
import requests
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

class AdminThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminTheme
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_css_url(self, value):
        if not value:
            return value

        base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
        try:
            if value.startswith('http://') or value.startswith('https://'):
                final_url = value
            else:
                final_url = f"{base_url}{staticfiles_storage.url(value.lstrip('/'))}"

            response = requests.head(final_url, timeout=5)
            response.raise_for_status()
            if 'text/css' not in response.headers.get('Content-Type', ''):
                raise serializers.ValidationError(f"Invalid CSS Content-Type for {value}")
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError(f"Invalid CSS URL: {value} - {e}")
        except ValueError as e:
            raise serializers.ValidationError(f"Validation error for CSS URL: {value} - {e}")
        return value

    def validate_js_url(self, value):
        if not value:
            return value

        base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
        try:
            if value.startswith('http://') or value.startswith('https://'):
                final_url = value
            else:
                final_url = f"{base_url}{staticfiles_storage.url(value.lstrip('/'))}"

            response = requests.head(final_url, timeout=5)
            response.raise_for_status()
            if 'application/javascript' not in response.headers.get('Content-Type', '') and \
               'text/javascript' not in response.headers.get('Content-Type', '') and \
               'application/x-javascript' not in response.headers.get('Content-Type', ''):
                raise serializers.ValidationError(f"Invalid JS Content-Type for {value}")
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError(f"Invalid JS URL: {value} - {e}")
        except ValueError as e:
            raise serializers.ValidationError(f"Validation error for JS URL: {value} - {e}")
        return value


class AdminThemeToggleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_active = serializers.BooleanField()

    def validate_id(self, value):
        try:
            AdminTheme.objects.get(pk=value)
        except AdminTheme.DoesNotExist:
            raise serializers.ValidationError("Theme with this ID does not exist.")
        return value