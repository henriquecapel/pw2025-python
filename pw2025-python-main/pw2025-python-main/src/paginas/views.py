from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, Group
from braces.views import GroupRequiredMixin

from .models import Cliente, Fotografo, Sessao
from .forms import UsuarioCadastroForm


class Inicio(TemplateView):
    template_name = "paginas/inicio.html"




#Páginas Sobreview, ClienteView, FotógrafoView e SessãoView

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'

class Clienteview(TemplateView):
    template_name = "paginas/cliente.html"

class Fotografoview(TemplateView):
    template_name = "paginas/fotografo.html"

class Sessãoview(TemplateView):
    template_name = "paginas/sessao.html"
    


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
    template_name = "paginas/login.html"
    success_url = reverse_lazy("login")
    success_message = "Usuário cadastrado com sucesso!"
    extra_context = {"titulo": "Cadastro de Cliente", 'botao': 'Cadastrar'}

    def form_valid(self, form):
        url = super().form_valid(form)
        grupo, _ = Group.objects.get_or_create(name="Cliente")
        self.object.groups.add(grupo)
        Cliente.objects.get_or_create(user=self.object)
        return url


# class CadastroFotografoView(SuccessMessageMixin, CreateView):
#     model = User
#     form_class = UsuarioCadastroForm
#     template_name = "paginas/form.html"
#     success_url = reverse_lazy("login")
#     success_message = "Usuário fotógrafo cadastrado com sucesso!"
#     extra_context = {"titulo": "Cadastrar fotógrafo"}

#     def form_valid(self, form):
#         url = super().form_valid(form)
#         grupo, _ = Group.objects.get_or_create(name="Fotógrafo")
#         self.object.groups.add(grupo)
#         Fotografo.objects.get_or_create(user=self.object)
#         return url

########################################################################## CREATE ###############

class ClienteCreate(LoginRequiredMixin, CreateView):

    model = Cliente
    fields = ["nome", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-clientes")
    extra_context = {"titulo": "Cadastrar cliente", "botao": "Cadastrar"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
class FotografoCreate(LoginRequiredMixin, CreateView):
    model = Fotografo
    fields = ["nome", "especialidade", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-fotografos")
    extra_context = {"titulo": "Cadastrar fotógrafo", "botao": "Cadastrar"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class SessaoCreate(UserOwnedQuerysetMixin, CreateView):
    model = Sessao
    fields = ["data", "horario", "duracao", "tipo", "valor", "finalizado", "cliente", "fotografo"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-sessoes")
    extra_context = {"titulo": "Cadastrar sessão",
                     'botao': 'Cadastrar'}


########################################################################### UPDATE#############

class ClienteUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = ["Cliente", "Admin"]
    model = Cliente
    fields = ["nome", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-clientes")
    extra_context = {"titulo": "Editar cliente",
                     'botao': 'Salvar'}

    def get_object(self, queryset=None):
        return get_object_or_404(Cliente, pk=self.kwargs["pk"])


class FotografoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = ["Fotógrafo", "Admin"]
    model = Fotografo
    fields = ["nome", "especialidade", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-fotografos")
    extra_context = {"titulo": "Editar fotógrafo",
                     'botao': 'Salvar'}

    def get_object(self, queryset=None):
        return get_object_or_404(Fotografo, pk=self.kwargs["pk"], user=self.request.user)

class SessaoUpdate(UserOwnedQuerysetMixin, UpdateView):
    model = Sessao
    fields = ["data", "horario", "duracao", "tipo", "valor", "finalizado", "cliente", "fotografo"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("excluir-sessoes")
    extra_context = {"titulo": "Editar sessão",
                     'botao': 'Salvar'}

########################################################################### DELETE#############

class ClienteDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = ["Cliente", "Admin"]
    model = Cliente
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-clientes")
    extra_context = {"titulo": "Excluir cliente",
                     'botao': 'Excluir'}

    def get_object(self, queryset=None):
        qs = Cliente.objects.all()
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            qs = qs.filter(user=self.request.user)
        return get_object_or_404(qs, pk=self.kwargs["pk"])


class FotografoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = ["Fotógrafo", "Admin"]
    model = Fotografo
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-fotografos")
    extra_context = {"titulo": "Excluir fotógrafo",
                     'botao': 'Excluir'}

    def get_object(self, queryset=None):
        return get_object_or_404(Fotografo, pk=self.kwargs["pk"], user=self.request.user)


class SessaoDelete(UserOwnedQuerysetMixin, DeleteView):
    model = Sessao
    template_name = "paginas/form.html"
    success_url = reverse_lazy("listar-sessoes")
    extra_context = {"titulo": "Excluir sessão",
                     'botao': 'Excluir'}

    def get_object(self, queryset=None):
        return get_object_or_404(
            Sessao,
            pk=self.kwargs["pk"],
            cadastrado_por=self.request.user,
        )

############################################################################ LIST #############


class ClienteList(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "paginas/cliente_list.html"
    context_object_name = "objetos"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Cliente.objects.all()
        return Cliente.objects.filter(user=self.request.user)

class FotografoList(LoginRequiredMixin, ListView):
    model = Fotografo
    template_name = "paginas/fotografo_list.html"
    context_object_name = "objetos"

    def get_queryset(self):
        return Fotografo.objects.filter(user=self.request.user)

class SessaoList(UserOwnedQuerysetMixin, ListView):
    model = Sessao
    template_name = "paginas/sessao_list.html"
    context_object_name = "objetos"







