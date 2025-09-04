from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    Inicio,
    ClienteList, FotografoList, EstudioList, SessaoFotoList,
    ClienteCreate, ClienteUpdate, ClienteDelete,
    FotografoCreate, FotografoUpdate, FotografoDelete,
    EstudioCreate, EstudioUpdate, EstudioDelete,
    SessaoFotoCreate, SessaoFotoUpdate, SessaoFotoDelete,
    CadastroClienteView, CadastroFotografoView,
)

urlpatterns = [
    path("", Inicio.as_view(), name="inicio"),

    path("registrar/cliente/", CadastroClienteView.as_view(), name="registrar-cliente"),
    path("registrar/fotografo/", CadastroFotografoView.as_view(), name="registrar-fotografo"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="paginas/form.html",
            extra_context={"titulo": "Autenticação", "botao": "Entrar"},
        ),
        name="login",
    ),
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

    path("clientes/", ClienteList.as_view(), name="clientes"),
    path("fotografos/", FotografoList.as_view(), name="fotografos"),
    path("estudios/", EstudioList.as_view(), name="estudios"),
    path("sessoes/", SessaoFotoList.as_view(), name="sessoes"),

    path("adicionar/cliente/", ClienteCreate.as_view(), name="inserir-cliente"),
    path("editar/cliente/<int:pk>/", ClienteUpdate.as_view(), name="editar-cliente"),
    path("excluir/cliente/<int:pk>/", ClienteDelete.as_view(), name="excluir-cliente"),

    path("adicionar/fotografo/", FotografoCreate.as_view(), name="inserir-fotografo"),
    path("editar/fotografo/<int:pk>/", FotografoUpdate.as_view(), name="editar-fotografo"),
    path("excluir/fotografo/<int:pk>/", FotografoDelete.as_view(), name="excluir-fotografo"),

    path("adicionar/estudio/", EstudioCreate.as_view(), name="inserir-estudio"),
    path("editar/estudio/<int:pk>/", EstudioUpdate.as_view(), name="editar-estudio"),
    path("excluir/estudio/<int:pk>/", EstudioDelete.as_view(), name="excluir-estudio"),

    path("adicionar/sessao/", SessaoFotoCreate.as_view(), name="inserir-sessao"),
    path("editar/sessao/<int:pk>/", SessaoFotoUpdate.as_view(), name="editar-sessao"),
    path("excluir/sessao/<int:pk>/", SessaoFotoDelete.as_view(), name="excluir-sessao"),
]
