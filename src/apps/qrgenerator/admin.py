from django.contrib import admin
from .models import Website

class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'url', 'qr_code')
    #Auto Grabs URLS for QR generation
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].choices = [(t, t) for t in Website.get_user_urls()]
        return form

admin.site.register(Website, WebsiteAdmin)