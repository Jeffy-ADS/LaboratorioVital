# Generated by Django 5.1.7 on 2025-03-21 13:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TiposExames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('tipo', models.CharField(choices=[('I', 'Exame de imagem'), ('S', 'Exame de Sangue')], max_length=2)),
                ('preco', models.FloatField()),
                ('disponivel', models.BooleanField(default=True)),
                ('horario_inicial', models.IntegerField()),
                ('horario_final', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SolicitacaoExame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('E', 'Em análise'), ('F', 'Finalizado')], max_length=2)),
                ('resultado', models.FileField(blank=True, null=True, upload_to='resultados')),
                ('requer_senha', models.BooleanField(default=False)),
                ('senha', models.CharField(blank=True, max_length=6, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('exame', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exames.tiposexames')),
            ],
        ),
        migrations.CreateModel(
            name='PedidosExames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agendado', models.BooleanField(default=True)),
                ('data', models.DateField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('exames', models.ManyToManyField(to='exames.solicitacaoexame')),
            ],
        ),
    ]
