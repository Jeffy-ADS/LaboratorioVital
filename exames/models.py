from datetime import timedelta, timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from secrets import token_urlsafe

# Classe que representa os tipos de exames disponíveis
class TiposExames(models.Model):
    tipo_choices = (
        ('I', 'Exame de imagem'),
        ('S', 'Exame de Sangue')
    )
    nome = models.CharField(max_length=50)  # Nome do exame
    tipo = models.CharField(max_length=2, choices=tipo_choices)  # Tipo do exame (imagem ou sangue)
    preco = models.FloatField()  # Preço do exame
    disponivel = models.BooleanField(default=True)  # Disponibilidade do exame
    horario_inicial = models.IntegerField()  # Horário inicial para realização do exame
    horario_final = models.IntegerField()  # Horário final para realização do exame

    def __str__(self):
        return self.nome  # Retorna o nome do exame ao exibir a instância


# Classe que representa uma solicitação de exame feita pelo usuário
class SolicitacaoExame(models.Model):
    choice_status = (
        ('E', 'Em análise'),
        ('F', 'Finalizado')
    )
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # Usuário que solicitou o exame
    exame = models.ForeignKey(TiposExames, on_delete=models.DO_NOTHING)  # Tipo de exame solicitado
    status = models.CharField(max_length=2, choices=choice_status)  # Status da solicitação
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)  # Arquivo com o resultado do exame
    requer_senha = models.BooleanField(default=False)  # Se o resultado requer senha para acesso
    senha = models.CharField(max_length=6, null=True, blank=True)  # Senha para acesso ao exame (opcional)

    def __str__(self):
        return f'{self.usuario} | {self.exame.nome}'  # Exibição do usuário e nome do exame
# Função auxiliar para gerar um "badge" (etiqueta visual) para o status do exame
    def badge_template(self):
        if self.status == 'E':
            classes_css = 'bg-warning text-dark'
            texto = "Em análise"
        elif self.status == 'F':
            classes_css = 'bg-success'
            texto = "Finalizado"
        else:
            classes_css = 'bg-secondary'
            texto = 'Indefinido'
        
        return mark_safe(f"<span class='badge bg-primary {classes_css}'>{texto}</span>")






# Classe que representa um pedido de múltiplos exames
class PedidosExames(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # Usuário que fez o pedido
    exames = models.ManyToManyField(SolicitacaoExame)  # Exames incluídos no pedido
    agendado = models.BooleanField(default=True)  # Indica se o pedido já foi agendado
    data = models.DateField()  # Data do pedido

    def __str__(self):
        return f'{self.usuario} | {self.data}'  # Exibição do usuário e data do pedido

# Classe que representa o acesso médico a exames de um paciente
class AcessoMedico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # Usuário ao qual o acesso é concedido
    identificacao = models.CharField(max_length=50)  # Identificação do médico
    tempo_de_acesso = models.IntegerField()  # Tempo de acesso permitido (em horas)
    criado_em = models.DateTimeField()  # Data e hora da criação do acesso
    data_exames_iniciais = models.DateField()  # Data inicial dos exames acessíveis
    data_exames_finais = models.DateField()  # Data final dos exames acessíveis
    token = models.CharField(max_length=20)  # Token de acesso

    def __str__(self):
        return self.token  # Exibe o token como representação da instância

    def save(self, *args, **kwargs):
        if not self.token:  # Se não houver token gerado, cria um novo automaticamente
            self.token = token_urlsafe(6)

        super(AcessoMedico, self).save(*args, **kwargs)  # Chama o método save da classe pai

    # Propriedade que retorna o status do acesso (Ativo ou Expirado)
    @property
    def status(self):
        return 'Expirado' if timezone.now() > (self.criado_em + timedelta(hours=self.tempo_de_acesso)) else 'Ativo'

    # Propriedade que gera uma URL de acesso médico baseada no token gerado
    @property
    def url(self):
        # TODO: Melhorar utilizando reverse para gerar a URL dinamicamente
        return f"http://127.0.0.1:8000/exames/acesso_medico/{self.token}"
