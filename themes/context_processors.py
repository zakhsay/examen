from .models import AdminTheme, UserThemePreference

def theme_urls(request):
    from .models import AdminTheme, UserThemePreference
    theme = None
    if request.user.is_authenticated:
        pref = UserThemePreference.objects.filter(user=request.user).first()
        if pref:
            theme = pref.theme
    if not theme:
        theme = AdminTheme.objects.filter(is_active=True).first()
    return {
        "theme_css_url": theme.css_url if theme else None,
        "theme_js_url": theme.js_url if theme else None,
    }

def active_theme(request):
    theme = None
    if request.user.is_authenticated:
        pref = UserThemePreference.objects.filter(user=request.user).first()
        if pref and pref.theme:
            theme = pref.theme
    if not theme:
        preview_id = request.session.get('preview_theme_id')
        if preview_id:
            theme = AdminTheme.objects.filter(id=preview_id).first()
    if not theme:
        theme = AdminTheme.objects.filter(is_active=True).first()
    return {'active_theme': theme}