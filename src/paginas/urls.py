from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("", Inicio.as_view(), name="inicio"),
    path('sobre/', SobreView.as_view(), name='sobre'),  # Página sobre


    path('login/', auth_views.LoginView.as_view(
        template_name = 'paginas/login.html',
        extra_context = {
          'titulo': 'Login',
          'botao': 'Entrar',
        }
    ), name='login'),


    path("sair/", auth_views.LogoutView.as_view(), name="logout"),

    path(
        "senha/",
        auth_views.PasswordChangeView.as_view(
            template_name="paginas/form.html",
            extra_context={"titulo": "Atualizar senha", "botao": "Salvar"},
        ),
        name="alterar-senha",
    ),
    path(
        "senha/ok/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="paginas/form.html",
            extra_context={"titulo": "Senha alterada", "botao": "OK"},
        ),
        name="password_change_done",
    ),

    path("cadastrar/usuario/", CadastroClienteView.as_view(), name="cadastrar-usuario"),

    path("cadastrar/cliente/", ClienteCreate.as_view(), name="cadastrar-cliente"),
    path("cadastrar/fotografo/", FotografoCreate.as_view(), name="cadastrar-fotografo"),
    path("cadastrar/sessao/", SessaoCreate.as_view(), name="cadastrar-sessao"),


    path("editar/cliente/<int:pk>/", ClienteUpdate.as_view(), name="editar-cliente"),
    path("editar/fotografo/<int:pk>/", FotografoUpdate.as_view(), name="editar-fotografo"),
    path("editar/sessao/<int:pk>/", SessaoUpdate.as_view(), name="editar-sessao"),


    path("excluir/cliente/<int:pk>/", ClienteDelete.as_view(), name="excluir-cliente"),
    path("excluir/fotografo/<int:pk>/", FotografoDelete.as_view(), name="excluir-fotografo"),
    path("excluir/sessao/<int:pk>/", SessaoDelete.as_view(), name="excluir-sessao"),


    path("listar/clientes/", ClienteList.as_view(), name="listar-clientes"),
    path("listar/fotografos/", FotografoList.as_view(), name="listar-fotografos"),
    path("listar/sessoes/", SessaoList.as_view(), name="listar-sessoes"), 
]
