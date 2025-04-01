from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import AcessoMedico, PedidosExames, SolicitacaoExame, TiposExames
from django.contrib import messages
from django.contrib.messages import constants

# Função para solicitar exames disponíveis
@login_required  # Requer que o usuário esteja autenticado
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()  # Obtém todos os tipos de exames disponíveis

    if request.method == "GET":
        # Renderiza a página com os tipos de exames
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    else:
        exames_id = request.POST.getlist('exames')  # Obtém os IDs dos exames selecionados

        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)  # Filtra os exames selecionados

        # Calcula o preço total dos exames
        preco_total = sum(exame.preco for exame in solicitacao_exames)

        # Renderiza a página novamente com os exames selecionados e o preço total
        return render(request, 'solicitar_exames.html', {
            'solicitacao_exames': solicitacao_exames, 
            'preco_total': preco_total, 
            'tipos_exames': tipos_exames
        })

# Função para fechar e registrar um pedido de exame
@login_required
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')  # Obtém os exames selecionados
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)  # Filtra os exames no banco de dados

    # Cria um novo pedido de exames para o usuário autenticado
    pedido_exame = PedidosExames(
        usuario=request.user,
        data=datetime.now()
    )
    pedido_exame.save()  # Salva o pedido no banco

    # Para cada exame selecionado, cria uma solicitação associada ao pedido
    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status="E"  # Define o status como "Em análise"
        )
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)  # Associa a solicitação ao pedido
    
    pedido_exame.save()  # Salva novamente para garantir a associação

    messages.add_message(request, constants.SUCCESS, 'Pedido de exame concluído com sucesso')
    return redirect('/exames/ver_pedidos/')

# Função para visualizar os pedidos de exames do usuário
@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)  # Obtém os pedidos do usuário
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})

# Função para cancelar um pedido de exame
@login_required
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id=pedido_id)  # Obtém o pedido pelo ID

    if pedido.usuario != request.user:  # Verifica se o pedido pertence ao usuário autenticado
        messages.add_message(request, constants.ERROR, 'Esse pedido não é seu')
        return redirect('/exames/gerenciar_pedidos/')

    pedido.agendado = False  # Marca o pedido como não agendado
    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido excluído com sucesso')
    return redirect('/exames/gerenciar_pedidos/')

# Função para visualizar exames do usuário
@login_required
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)  # Obtém os exames do usuário
    return render(request, 'gerenciar_exames.html', {'exames': exames})

# Função para solicitar acesso ao resultado de um exame protegido por senha
@login_required
def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)  # Obtém o exame pelo ID

    if request.method == "GET":
        return render(request, 'solicitar_senha_exame.html', {'exame': exame})
    elif request.method == "POST":
        senha = request.POST.get("senha")

        # TODO: validar se o exame pertence ao usuário

        if senha == exame.senha:  # Verifica se a senha digitada está correta
            return redirect(exame.resultado.url)  # Redireciona para o arquivo do resultado
        else:
            messages.add_message(request, constants.ERROR, 'Senha inválida')
            return redirect(f'/exames/solicitar_senha_exame/{exame.id}')

# Função para gerar um acesso médico, permitindo que médicos vejam exames do usuário
@login_required    
def gerar_acesso_medico(request):
    if request.method == "GET":
        acessos_medicos = AcessoMedico.objects.filter(usuario=request.user)  # Obtém acessos médicos do usuário
        return render(request, 'gerar_acesso_medico.html', {'acessos_medicos': acessos_medicos})
    
    elif request.method == "POST":
        identificacao = request.POST.get('identificacao')
        tempo_de_acesso = request.POST.get('tempo_de_acesso')
        data_exame_inicial = request.POST.get("data_exame_inicial")
        data_exame_final = request.POST.get("data_exame_final")

        # Cria um novo acesso médico
        acesso_medico = AcessoMedico(
            usuario=request.user,
            identificacao=identificacao,
            tempo_de_acesso=tempo_de_acesso,
            data_exames_iniciais=data_exame_inicial,
            data_exames_finais=data_exame_final,
            criado_em=datetime.now()
        )

        acesso_medico.save()  # Salva no banco de dados

        messages.add_message(request, constants.SUCCESS, 'Acesso gerado com sucesso')
        return redirect('/exames/gerar_acesso_medico')

# Função para acessar exames usando um token gerado para médicos
def acesso_medico(request, token):
    acesso_medico = AcessoMedico.objects.get(token=token)  # Obtém o acesso pelo token

    if acesso_medico.status == 'Expirado':  # Verifica se o link ainda é válido
        messages.add_message(request, constants.WARNING, 'Esse link já expirou!')
        return redirect('/usuarios/login')

    # Filtra os pedidos de exames dentro do período permitido pelo acesso médico
    pedidos = PedidosExames.objects.filter(
        data__gte=acesso_medico.data_exames_iniciais
    ).filter(
        data__lte=acesso_medico.data_exames_finais
    ).filter(
        usuario=acesso_medico.usuario
    )

    return render(request, 'acesso_medico.html', {'pedidos': pedidos})
