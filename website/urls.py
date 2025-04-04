from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_website, name='home_website'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('exames/', views.exames, name='exames'),
    path('unidades/', views.unidades, name='unidades'),
    path('resultados/', views.resultados, name='resultados'),
    path('convenios/', views.convenios, name='convenios'),
    path('contato/', views.contato, name='contato'),
]