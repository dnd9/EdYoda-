from django.contrib import admin
from .models import MusicFile, User, AllowedEmail


admin.site.register(User)
admin.site.register(MusicFile)
admin.site.register(AllowedEmail)