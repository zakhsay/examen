from django.core.exceptions import ValidationError

def validate_css_js_url(value):
    if not value.endswith(('.css', '.js')):
        raise ValidationError("URL must end with .css or .js")
