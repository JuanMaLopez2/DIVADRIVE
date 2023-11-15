from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import UserCreateForm, UserRecoverForm
from .models import UserProfile


def signupaccount(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                
                # Crea el UserProfile asociado al usuario
                profile_picture = form.cleaned_data['profile_picture']
                UserProfile.objects.create(user=user, profile_picture=profile_picture)

                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html', {'form': form, 'error': 'Username already taken. Choose a new username.'})
    else:
        form = UserCreateForm()
    return render(request, 'signupaccount.html', {'form': form})

'''def signupaccount(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html', {'form': form, 'error': 'Username already taken. Choose a new username.'})
    else:
        form = UserCreateForm()
    return render(request, 'signupaccount.html', {'form': form})'''

@login_required
def logoutaccount(request):
    logout(request)
    return redirect('home')

def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form': AuthenticationForm})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'loginaccount.html', {'form': AuthenticationForm(), 'error': 'Username and password do not match'})
        else:
            login(request, user)
            return redirect('home')
    elif request.method == 'POST':
        # Agrega aquí la lógica para recuperar contraseñas
        return redirect('recoverpassword')
    else:
        return render(request, 'loginaccount.html', {'form': AuthenticationForm()})

def recoverPassword(request):
    if request.method == 'POST':
        form = UserRecoverForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            new_password = form.cleaned_data['password']
            try:
                user = get_user_model().objects.get(username=username)
            except get_user_model().DoesNotExist:
                return render(request, 'recover.html', {'form': UserRecoverForm(), 'error': 'User doesn\'t exist'})

            # Cambiar la contraseña del usuario
            user.set_password(new_password)
            user.save()

            # Autenticar al usuario con la nueva contraseña
            user = authenticate(request, username=username, password=new_password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserRecoverForm()

    return render(request, 'recover.html', {'form': form})
