from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

class BookrAdmin(admin.AdminSite):
    site_header = "Bookr Administration Portal LAB10"
    site_title =  "Bookr Administration Portal"
    index_title = "Bookr Administration "
    logout_template = 'admin/logout.html'

    def profile_view(self, request):
        request.current_app = self.name
        context = self.each_context(request)
        return TemplateResponse(request, "admin/admin_profile.html", context)

    def get_urls(self):
        urls = super().get_urls()
        return [path("admin_profile/", self.admin_view(self.profile_view))] + urls
