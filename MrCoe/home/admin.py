from django.contrib import admin
from .models import HoneypotHit

@admin.register(HoneypotHit)
class HoneypotHitAdmin(admin.ModelAdmin):
    list_display = ("ip", "method", "path", "timestamp", "count")
    search_fields = ("ip", "user_agent")
    list_filter = ("method", "timestamp")