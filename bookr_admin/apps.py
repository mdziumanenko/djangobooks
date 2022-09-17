# from django.apps import AppConfig
# class BookrAdminConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'bookr_admin'

from django.contrib.admin.apps import AdminConfig
class BookrAdminConfig(AdminConfig):
    default_site = 'bookr_admin.admin.BookrAdmin'