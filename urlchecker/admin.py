from django.contrib import admin
from .models import URLCheck


@admin.register(URLCheck)
class URLCheckAdmin(admin.ModelAdmin):
    list_display = ('url', 'result', 'checked_at')
    list_filter = ('result', 'checked_at')
    search_fields = ('url',)
    ordering = ('-checked_at',)