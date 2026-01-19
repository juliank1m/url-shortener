from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Link

# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("code", "short_link", "is_active", "target_url", "clicks", "created_at", "last_clicked_at")
    search_fields = ("code", "target_url")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    readonly_fields = ("short_link", "created_at", "clicks", "last_clicked_at")

    fieldsets = (
        (None, {"fields": ("short_link", "target_url", "is_active")}),
        ("Metadata", {"fields": ("code", "created_at", "clicks", "last_clicked_at")}),
    )

    @admin.display(description="Short link")
    def short_link(self, obj):
        if not obj or not obj.pk or not obj.code:
            return "(will appear after saving)"

        path = reverse("redirect_link", kwargs={"code": obj.code})
        return format_html('<a href="{}" target="_blank">{}</a>', path, path)

    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            ro.append("code")
        return ro

