# Generated by Django 5.1.7 on 2025-04-01 12:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exames", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AcessoMedico",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("identificacao", models.CharField(max_length=50)),
                ("tempo_de_acesso", models.IntegerField()),
                ("criado_em", models.DateTimeField()),
                ("data_exames_iniciais", models.DateField()),
                ("data_exames_finais", models.DateField()),
                ("token", models.CharField(max_length=20)),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
