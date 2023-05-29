from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index', views.homepage, name='homepage'),
    path('upload/', views.share_music, name='upload_music'),
    path('', views.user_login, name='login'),
      path('logout', auth_views.LogoutView.as_view(), name= 'logout'),
    path('register', views.register, name = 'register'),
    path('protected-file-allowed-emails/<int:file_id>/', views.protected_file_allowed_emails, name='protected_file_allowed_emails'),
]
