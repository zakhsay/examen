from django.contrib import admin
from .models import AdminTheme

class AdminThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    actions = ['make_active']

    def make_active(self, request, queryset):
        AdminTheme.objects.update(is_active=False)
        theme = queryset.first()
        if theme:
            theme.is_active = True
            theme.save()
            self.message_user(request, f"'{theme.name}' is now the active theme.")
        else:
            self.message_user(request, "No theme selected.", level='error')
    make_active.short_description = "Set selected theme as active (only one can be active)"

admin.site.register(AdminTheme, AdminThemeAdmin)
# Register your models here.
