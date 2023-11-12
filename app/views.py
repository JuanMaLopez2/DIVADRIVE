from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StartTrip
from .models import Trip

@login_required
def home(request):
    if request.method == 'POST':
        formulario = StartTrip(request.POST)
        if formulario.is_valid():
            # Obtén los datos del formulario y asigna el usuario actual
            destino_lat = formulario.cleaned_data['destination_lat']
            destino_lon = formulario.cleaned_data['destination_lon']
            origen_lat = formulario.cleaned_data['origin_lat']
            origen_lon = formulario.cleaned_data['origin_lon']

            objeto = Trip(
                user=request.user,
                destination_lat=destino_lat,
                destination_lon=destino_lon,
                origin_lat=origen_lat,
                origin_lon=origen_lon,
            )
            objeto.save()

            return redirect('home')  # Redirige a la misma vista o a donde desees
    else:
        formulario = StartTrip()

    # Obtén las coordenadas de destino específicas para el usuario actual
    destino_usuario = Trip.objects.filter(user=request.user).last()
    contexto = {
        'formulario': formulario,
    }

    if destino_usuario:
        contexto['destino_lat'] = destino_usuario.destination_lat
        contexto['destino_lon'] = destino_usuario.destination_lon
    else:
        # Si no hay destino para el usuario, obtén las coordenadas del último viaje
        ultimo_viaje = Trip.objects.last()
        if ultimo_viaje:
            contexto['destino_lat'] = ultimo_viaje.destination_lat
            contexto['destino_lon'] = ultimo_viaje.destination_lon

    return render(request, 'home.html', contexto)

def welcome(request):
    return render(request, 'welcome.html')
