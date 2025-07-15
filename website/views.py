from django.shortcuts import render


def labtech(request):
    return render(request, 'website/labtech.html')

def home_website(request):
    return render(request, 'website/home_website.html')


def exames(request):
    return render(request, 'website/exames.html')

def unidades(request):
    return render(request, 'website/unidades.html')

def resultados(request):
    return render(request, 'website/resultados.html')

def convenios(request):
    return render(request, 'website/convenios.html')

def contato(request):
    return render(request, 'website/contato.html')

def location(request):
    return render(request, 'website/location.html')