from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import UserCreateForm, UserRecoverForm
from .models import UserProfile
from deepface import DeepFace
from django.http import HttpResponseServerError
from django.conf import settings
import os

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
            try:
                # Check if the profile picture is present in the request
                if 'profile_picture' in request.FILES:
                    # Get the profile picture from the request
                    input_image = request.FILES['profile_picture']
                    #input_image = os.path.join(settings.MEDIA_ROOT, str(user.userprofile.profile_picture))
                    temp_file_path = 'temp_image.jpg'
                    with open(temp_file_path, 'wb') as temp_file:
                        for chunk in input_image.chunks():
                            temp_file.write(chunk)

                    # Get the stored profile picture path from the user's profile
                    stored_image_path = os.path.join(settings.MEDIA_ROOT,str(user.userprofile.profile_picture))

                    try:
                        # Compare the images using DeepFace
                        result = DeepFace.verify(temp_file_path, stored_image_path)
                        # Check if the images match
                        if result['verified']:
                            login(request, user)
                            return redirect('home')
                        else:
                            return render(request, 'loginaccount.html', {'form': AuthenticationForm(), 'error': 'Profile picture does not match'})
                    except Exception as deepface_error:
                        # Log the DeepFace error for debugging purposes
                        print(f"Error during image comparison with DeepFace: {str(deepface_error)}")
                        return HttpResponseServerError(f"Error during image comparison with DeepFace: {str(deepface_error)}")
                    finally:
                        # Asegúrate de eliminar el archivo temporal después de usarlo si es necesario
                        os.remove(temp_file_path)
                else:
                    # Handle the case where the user did not upload a profile picture during login
                    return render(request, 'loginaccount.html', {'form': AuthenticationForm(), 'error': 'Profile picture is required for login'})
            except Exception as e:
                # Log other errors for debugging purposes
                print(f"Error during login: {str(e)}")
                return HttpResponseServerError('Error during login. Please try again or contact support.')
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
