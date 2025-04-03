from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import redirect, render

from .models import AcessoMedico, PedidosExames, SolicitacaoExame, TiposExames


# ================== PEDIDOS DE EXAMES ==================

# Função para solicitar exames disponíveis
@login_required
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()

    if request.method == "GET":
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

    preco_total = sum(i.preco for i in solicitacao_exames)

    return render(request, 'solicitar_exames.html', {
        'solicitacao_exames': solicitacao_exames,
        'preco_total': preco_total,
        'tipos_exames': tipos_exames
    })


# Função para fechar e registrar um pedido de exame
@login_required
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

    pedido_exame = PedidosExames(usuario=request.user, data=datetime.now())
    pedido_exame.save()

    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(usuario=request.user, exame=exame, status="E")
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)

    pedido_exame.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de exame concluído com sucesso')
    return redirect('/exames/gerenciar_pedidos/')


# Função para visualizar os pedidos de exames do usuário
@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})


# Função para cancelar um pedido de exame
@login_required
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id=pedido_id)

    if pedido.usuario != request.user:
        messages.add_message(request, constants.ERROR, 'Esse pedido não é seu')
        return redirect('/exames/gerenciar_pedidos/')

    pedido.agendado = False
    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido excluído com sucesso')
    return redirect('/exames/gerenciar_pedidos/')


# ================== GERENCIAMENTO DE EXAMES ==================

# Função para visualizar exames do usuário
@login_required
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_exames.html', {'exames': exames})


# Função para permitir abrir um exame
@login_required
def permitir_abrir_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    # TODO: validar se o exame pertence ao usuário
    if not exame.requer_senha:
        return redirect(exame.resultado.url)
    
    return redirect(f'/exames/solicitar_senha_exame/{exame.id}')


# Função para solicitar acesso ao resultado de um exame protegido por senha
@login_required
def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    if request.method == "GET":
        return render(request, 'solicitar_senha_exame.html', {'exame': exame})
    
    senha = request.POST.get("senha")

    # TODO: validar se o exame pertence ao usuário
    if senha == exame.senha:
        return redirect(exame.resultado.url)
    
    messages.add_message(request, constants.ERROR, 'Senha inválida')
    return redirect(f'/exames/solicitar_senha_exame/{exame.id}')


# ================== ACESSO MÉDICO ==================

# Função para gerar um acesso médico
@login_required
def gerar_acesso_medico(request):
    if request.method == "GET":
        acessos_medicos = AcessoMedico.objects.filter(usuario=request.user)
        return render(request, 'gerar_acesso_medico.html', {'acessos_medicos': acessos_medicos})
    
    identificacao = request.POST.get('identificacao')
    tempo_de_acesso = request.POST.get('tempo_de_acesso')
    data_exame_inicial = request.POST.get("data_exame_inicial")
    data_exame_final = request.POST.get("data_exame_final")

    acesso_medico = AcessoMedico(
        usuario=request.user,
        identificacao=identificacao,
        tempo_de_acesso=tempo_de_acesso,
        data_exames_iniciais=data_exame_inicial,
        data_exames_finais=data_exame_final,
        criado_em=datetime.now()
    )
    acesso_medico.save()

    messages.add_message(request, constants.SUCCESS, 'Acesso gerado com sucesso')
    return redirect('/exames/gerar_acesso_medico')


# Função para acessar exames usando um token gerado para médicos
def acesso_medico(request, token):
    acesso_medico = AcessoMedico.objects.get(token=token)

    if acesso_medico.status == 'Expirado':
        messages.add_message(request, constants.WARNING, 'Esse link já expirou!')
        return redirect('/usuarios/login')

    pedidos = PedidosExames.objects.filter(
        data__gte=acesso_medico.data_exames_iniciais,
        data__lte=acesso_medico.data_exames_finais,
        usuario=acesso_medico.usuario
    )

    return render(request, 'acesso_medico.html', {'pedidos': pedidos})
