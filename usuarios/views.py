from django.contrib.auth import authenticate, login, logout  # Importa funções de autenticação
from django.contrib.messages import constants  # Importa constantes para mensagens de feedback
from django.shortcuts import render, redirect  # Importa funções para renderizar templates e redirecionar
from django.contrib.auth.models import User  # Importa o modelo User para criar novos usuários
from django.contrib import messages  # Importa o módulo de mensagens de feedback

# Função que exibe a página inicial
def home(request):
    # Se o usuário estiver autenticado, passa o nome dele para o template
    if request.user.is_authenticated:
        nome = request.user.first_name
        return render(request, 'home.html', {'nome': nome})  # Renderiza o template 'home.html' com o nome do usuário
    # Se o usuário não estiver autenticado, apenas renderiza o template sem dados adicionais
    return render(request, 'home.html')

# Função de cadastro de novo usuário
def cadastro(request):
    # Se o usuário já estiver autenticado, redireciona para a página inicial
    if request.user.is_authenticated:
        return redirect('home')

    # Se a requisição for GET, exibe o formulário de cadastro
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        # Coleta os dados do formulário enviados via POST
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Verifica se as senhas são iguais
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')  # Adiciona mensagem de erro
            return redirect('cadastro')
        
        # Verifica se a senha tem pelo menos 6 caracteres
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'As senhas devem ter mais de 6 caracteres')  # Adiciona mensagem de erro
            return redirect('cadastro')
        
        try:
            # Cria um novo usuário, se o username não for duplicado
            User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
        except:  # Em caso de erro (como username duplicado)
            messages.add_message(request, constants.ERROR, 'Erro no servidor')  # Adiciona mensagem de erro
            return redirect('login')  # Redireciona para a página de login

        return redirect('cadastro')  # Se o cadastro for bem-sucedido, redireciona para a página de cadastro

# Função de login de usuário
def logar(request):
    # Se o usuário já estiver autenticado, redireciona para a página inicial
    if request.user.is_authenticated:
        return redirect('home')
        
    # Se a requisição for GET, exibe o formulário de login
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        # Coleta os dados de login (username e senha) enviados via POST
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        # Autentica o usuário usando o username e a senha
        user = authenticate(username=username, password=senha)

        if user:
            # Se a autenticação for bem-sucedida, faz o login do usuário
            login(request, user)
            # Redireciona o usuário para a página inicial (a linha abaixo pode causar erro, mas será corrigida posteriormente)
            return redirect('home')
        else:
            # Se a autenticação falhar, adiciona uma mensagem de erro
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('login')

# Função de logout
def sair(request):
    logout(request)  # Realiza o logout do usuário
    return redirect('/')  # Redireciona para a página inicial

