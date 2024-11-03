from django.urls import path
from .views import home, profile, RegisterView, upload_file, all_files

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('upload_file/', upload_file, name='upload_file'),
    path('all_files/', all_files, name='all_files'),
]
