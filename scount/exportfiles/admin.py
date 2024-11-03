from django.contrib import admin
from .models import Profile, UserFile


admin.site.register(Profile)

@admin.register(UserFile)
class UserFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'upload_date', 'user', 'file_name')