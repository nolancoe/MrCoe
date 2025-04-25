from django.contrib import admin
from .models import HoneypotHit, HoneypotCredential, BannedIP

@admin.register(HoneypotHit)
class HoneypotHitAdmin(admin.ModelAdmin):
    list_display = ("ip", "method", "path", "timestamp", "count")
    search_fields = ("ip", "user_agent", "path")
    list_filter = ("method", "timestamp")

@admin.register(HoneypotCredential)
class HoneypotCredentialAdmin(admin.ModelAdmin):
    list_display = ("ip", "username", "truncated_password", "timestamp")
    search_fields = ("ip", "username", "password")
    list_filter = ("timestamp",)
    readonly_fields = ("ip", "username", "password", "timestamp")

    def truncated_password(self, obj):
        return (obj.password[:30] + '...') if len(obj.password) > 30 else obj.password
    truncated_password.short_description = "Password"


@admin.register(BannedIP)
class BannedIPAdmin(admin.ModelAdmin):
    list_display = ('ip', 'jail', 'banned_at', 'location', 'org')
    search_fields = ('ip', 'jail', 'location','banned_at', 'org')