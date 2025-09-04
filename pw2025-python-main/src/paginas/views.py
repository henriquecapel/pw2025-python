from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Group

from .models import Cliente, Fotografo, Sessao
from .forms import UsuarioCadastroForm


ROLE_CLIENTE = "Cliente"
ROLE_FOTOGRAFO = "Fotógrafo"


class Inicio(TemplateView):
    template_name = "paginas/bootstrap.html"


class SobreView(TemplateView):
    template_name = "paginasweb/sobre.html"


class ClienteView(TemplateView):
    template_name = "paginas/cliente.html"


class FotografoView(TemplateView):
    template_name = "paginas/fotografo.html"


class SessaoView(TemplateView):
    template_name = "paginas/sessao.html"


class RoleValidatingLoginView(LoginView):
    template_name = "paginas/login.html"
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        self.role = kwargs.get("role")  # "cliente" | "fotografo"
        if self.role not in ("cliente", "fotografo"):
            messages.error(request, "Perfil de login inválido.")
            return redirect("inicio")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        required_group = ROLE_CLIENTE if self.role == "cliente" else ROLE_FOTOGRAFO
        other_group = ROLE_FOTOGRAFO if self.role == "cliente" else ROLE_CLIENTE

        if not user.groups.filter(name=required_group).exists():
            logout(self.request)
            messages.error(self.request, f"Este usuário não pertence ao grupo {required_group}.")
            return redirect("login-cliente" if self.role == "cliente" else "login-fotografo")

        if user.groups.filter(name=other_group).exists():
            logout(self.request)
            messages.error(self.request, "Este usuário está associado a mais de um perfil. Contate o administrador.")
            return redirect("login")

        return response

    def get_success_url(self):
        return reverse("listar-sessoes")


class UserOwnedQuerysetMixin(LoginRequiredMixin):
    owner_field = "cadastrado_por"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**{self.owner_field: self.request.user})

    def form_valid(self, form):
        if not form.instance.pk:
            setattr(form.instance, self.owner_field, self.request.user)
        return super().form_valid(form)


class CadastroClienteView(SuccessMessageMixin, CreateView):
    form_class = UsuarioCadastroForm
    template_name = "paginas/form.html"
    success_url = reverse_lazy("login-cliente")
    success_message = "Usuário cliente cadastrado com sucesso!"
    extra_context = {"titulo": "Cadastro de Cliente", "botao": "Cadastrar"}

    def form_valid(self, form):
        url = super().form_valid(form)
        g, _ = Group.objects.get_or_create(name=ROLE_CLIENTE)
        self.object.groups.add(g)
        Cliente.objects.get_or_create(user=self.object)
        return url


class CadastroFotografoView(SuccessMessageMixin, CreateView):
    form_class = UsuarioCadastroForm
    template_name = "paginas/form.html"
    success_url = reverse_lazy("login-fotografo")
    success_message = "Usuário fotógrafo cadastrado com sucesso!"
    extra_context = {"titulo": "Cadastro de Fotógrafo", "botao": "Cadastrar"}

    def form_valid(self, form):
        url = super().form_valid(form)
        g, _ = Group.objects.get_or_create(name=ROLE_FOTOGRAFO)
        self.object.groups.add(g)
        Fotografo.objects.get_or_create(user=self.object)
        return url


class ClienteCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = ["Admin", ROLE_CLIENTE]
    raise_exception = True
    model = Cliente
    fields = ["nome", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-clientes")
    extra_context = {"titulo": "Cadastrar cliente", "botao": "Cadastrar"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClienteUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [ROLE_CLIENTE, "Admin"]
    raise_exception = True
    model = Cliente
    fields = ["nome", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-clientes")
    extra_context = {"titulo": "Editar cliente", "botao": "Salvar"}

    def get_object(self, queryset=None):
        qs = Cliente.objects.all()
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            qs = qs.filter(user=self.request.user)
        return get_object_or_404(qs, pk=self.kwargs["pk"])


class ClienteDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = [ROLE_CLIENTE, "Admin"]
    raise_exception = True
    model = Cliente
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-clientes")
    extra_context = {"titulo": "Excluir cliente", "botao": "Excluir"}

    def get_object(self, queryset=None):
        qs = Cliente.objects.all()
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            qs = qs.filter(user=self.request.user)
        return get_object_or_404(qs, pk=self.kwargs["pk"])


class ClienteList(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "paginas/cliente_list.html"
    context_object_name = "objetos"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Cliente.objects.all()
        return Cliente.objects.filter(user=self.request.user)


class FotografoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = ["Admin", ROLE_FOTOGRAFO]
    raise_exception = True
    model = Fotografo
    fields = ["nome", "especialidade", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-fotografos")
    extra_context = {"titulo": "Cadastrar fotógrafo", "botao": "Cadastrar"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FotografoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [ROLE_FOTOGRAFO, "Admin"]
    raise_exception = True
    model = Fotografo
    fields = ["nome", "especialidade", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-fotografos")
    extra_context = {"titulo": "Editar fotógrafo", "botao": "Salvar"}

    def get_object(self, queryset=None):
        return get_object_or_404(Fotografo, pk=self.kwargs["pk"], user=self.request.user)


class FotografoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = [ROLE_FOTOGRAFO, "Admin"]
    raise_exception = True
    model = Fotografo
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-fotografos")
    extra_context = {"titulo": "Excluir fotógrafo", "botao": "Excluir"}

    def get_object(self, queryset=None):
        return get_object_or_404(Fotografo, pk=self.kwargs["pk"], user=self.request.user)


class FotografoList(LoginRequiredMixin, ListView):
    model = Fotografo
    template_name = "paginas/fotografo_list.html"
    context_object_name = "objetos"

    def get_queryset(self):
        return Fotografo.objects.filter(user=self.request.user)


class SessaoCreate(UserOwnedQuerysetMixin, CreateView):
    model = Sessao
    fields = ["data", "horario", "duracao", "tipo", "valor", "finalizado", "cliente", "fotografo"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-sessoes")
    extra_context = {"titulo": "Cadastrar sessão", "botao": "Cadastrar"}


class SessaoUpdate(UserOwnedQuerysetMixin, UpdateView):
    model = Sessao
    fields = ["data", "horario", "duracao", "tipo", "valor", "finalizado", "cliente", "fotografo"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-sessoes")
    extra_context = {"titulo": "Editar sessão", "botao": "Salvar"}


class SessaoDelete(UserOwnedQuerysetMixin, DeleteView):
    model = Sessao
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-sessoes")
    extra_context = {"titulo": "Excluir sessão", "botao": "Excluir"}

    def get_object(self, queryset=None):
        return get_object_or_404(Sessao, pk=self.kwargs["pk"], cadastrado_por=self.request.user)


class SessaoList(UserOwnedQuerysetMixin, ListView):
    model = Sessao
    template_name = "paginas/sessao_list.html"
    context_object_name = "objetos"
