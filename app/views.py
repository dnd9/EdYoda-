from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MusicFile, AllowedEmail
from .forms import Registration, Login, User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password


#user registration 
def register(request):
    if request.method =='POST':
        form = Registration(request.POST)
        # Validate username, email, and password.
        if form.is_valid():         
            user = form.save(commit= False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = Registration()
    context = {
        'form':form,
        }
    return render(request, 'musicshareapp/register.html', context)


def user_login(request):
    if request.method == "POST":
        form = Login(request.POST)
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        user = authenticate (request, email = email, password = password)
        
        if user.is_authenticated:
            login(request, user)  
            return redirect('homepage')
        else:
            error = "Wrong email or password"
            form = Login()
            context = {
            'form':form,
            'error': error, 
            }
            return render (request, 'musicshareapp/login.html', context)
    else:
        form = Login()
        context = {
            'form':form
        }
        return render (request, 'musicshareapp/login.html', context)


def homepage(request):
    # Retrieve music files accessible to the logged-in user
    public_music_files = MusicFile.objects.filter(file_access_level='public').prefetch_related('uploaded_by').order_by('-upload_date')

   
    uploaded_music_files = MusicFile.objects.filter(uploaded_by = request.user).order_by('-upload_date')
    protected_music_files = MusicFile.objects.prefetch_related('allowed_emails').filter(file_access_level= 'protected', allowed_emails__protected_file_allowed_emails__contains = request.user.email).order_by('-upload_date')
    context = {
        'public_music_files': public_music_files,
        'protected_music_files':protected_music_files, 
        'uploaded_music_files':uploaded_music_files
    }
    return render(request, 'musicshareapp/index.html', context)

#uplaoding music function renders a from and redirects to home page on success
def share_music(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        file_access_level = request.POST.get('file_access_level')
        music_file = request.FILES['file']
        song_file = MusicFile.objects.create(
                                title=title, 
                                artist = artist, 
                                music_file = music_file,
                                uploaded_by = request.user, 
                                file_access_level = file_access_level,
                            )
        
        if file_access_level == 'protected':         
            return redirect (protected_file_allowed_emails, file_id = song_file.id)
        return redirect('homepage')  
    else: 
        return render(request, 'musicshareapp/upload.html')

 
 #Function to process protected files, requests emails, Split the email input into a list of emails, checks for user availabilty and saves availbale users in a AllowedEmail model
def protected_file_allowed_emails(request, file_id):
    uploaded_file = MusicFile.objects.get( id = file_id ) 

    if request.method == 'POST':
        protected_file_allowed_emails = request.POST.get('protected_file_allowed_emails', '')


        email_list = [email.strip() for email in protected_file_allowed_emails.split(',')]

        registered_emails = User.objects.filter(email__in = email_list)

        for registered_email in registered_emails.values_list('email', flat=True):
            AllowedEmail.objects.create(music_file = uploaded_file, protected_file_allowed_emails = registered_email)
        return redirect('homepage')

    return render(request, 'musicshareapp/protected_emails.html', {'uploaded_file': uploaded_file})