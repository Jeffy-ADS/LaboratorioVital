from django.shortcuts import render

def home_website(request):
    return render(request, 'website/home_website.html')

def quem_somos(request):
    return render(request, 'website/quem_somos.html')

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