from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from django.contrib import messages
from .models import User
import uuid
from .utils import send_email_token
from django.http import HttpResponse 
def loginPage(request): 
    page = 'login'
    if request.user.is_authenticated:
        return redirect('participant_home') 

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password=password , email_verified=True)

        if user is not None:
            login(request, user)
            return redirect('participant_home') 
        else:
            messages.error(request, 'Email OR password does not exit') 
    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.username = user.username.lower()
            user.email_token = str(uuid.uuid4())
            send_email_token(user.email, user.email_token)
            user.save()
            messages.success(request, f'Email has been sent to {user.email}')
        else:
            messages.error(request, 'An error occurred during registration (Ensure that you are not using the same email id, this error could have been caused by that)')

    return render(request, 'login_register.html', {'form': form})


def participant_home(request):
    user_1= User.objects.get(email=str(request.user))
    context = {
        'user_1':user_1,
    }
    return render(request, 'participant_home.html', context)

def verify(request,token):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('participant_home')
    try:
        user = User.objects.get(email_token=token)
        user.email_verified = True
        user.save()
        messages.success(request, 'Email verified')
        login(request, user)
        return redirect('participant_home')
    except Exception as e:
        messages.error(request, 'Invalid request')
    
    return HttpResponse('verify')