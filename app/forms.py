from django.forms import ModelForm, PasswordInput
from .models import User, MusicFile

class Registration(ModelForm):
    class Meta:
        model = User
        fields= ['email', 'password']
        widgets={
            'password':PasswordInput
        }
        
class Login (ModelForm):
    class Meta:
        model= User
        fields=['email', 'password']
        widgets={
            "password" :PasswordInput
        }

