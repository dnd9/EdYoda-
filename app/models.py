from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    userid = models.AutoField(primary_key=True)
    email= models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    registration_date= models.DateTimeField(default= timezone.now)

    def __str__(self) -> str:
        return self.username
    

class MusicFile(models.Model):
    FILE_ACCESS_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected'),
    )
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    music_file = models.FileField(upload_to='/musicshareapp')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file_access_level = models.CharField(max_length=10, choices=FILE_ACCESS_CHOICES, default='public')
    upload_date = models.DateTimeField(default=timezone.now)  

    def __str__(self) -> str:
        return self.title

class AllowedEmail(models.Model):
    music_file = models.ForeignKey(MusicFile, on_delete=models.CASCADE, related_name='allowed_emails')
    protected_file_allowed_emails = models.EmailField(blank=True)

    def __str__(self) -> str:
        return self.protected_file_allowed_emails