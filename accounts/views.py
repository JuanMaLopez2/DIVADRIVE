from django.shortcuts import render
from .forms import UserCreateForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html',
            {'form':UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html',
                {'form':UserCreateForm,
                'error':'Username already taken. Choose new username.'})
        else:
            return render(request, 'signupaccount.html',
            {'form':UserCreateForm, 'error':'Passwords do not match'})

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

from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import render, redirect
from .forms import UserRecoverForm

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