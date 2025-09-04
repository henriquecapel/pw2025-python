from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, Group

from .models import Cliente, Fotografo, Estudio, SessaoFoto
from .forms import UsuarioCadastroForm


class Inicio(TemplateView):
    template_name = "paginas/index.html"


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
    model = User
    form_class = UsuarioCadastroForm
    template_name = "paginas/form.html"
    success_url = reverse_lazy("login")
    success_message = "Usuário cliente cadastrado com sucesso!"
    extra_context = {"titulo": "Cadastrar cliente"}

    def form_valid(self, form):
        url = super().form_valid(form)
        grupo, _ = Group.objects.get_or_create(name="Cliente")
        self.object.groups.add(grupo)
        Cliente.objects.get_or_create(user=self.object)
        return url


class CadastroFotografoView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UsuarioCadastroForm
    template_name = "paginas/form.html"
    success_url = reverse_lazy("login")
    success_message = "Usuário fotógrafo cadastrado com sucesso!"
    extra_context = {"titulo": "Cadastrar fotógrafo"}

    def form_valid(self, form):
        url = super().form_valid(form)
        grupo, _ = Group.objects.get_or_create(name="Fotógrafo")
        self.object.groups.add(grupo)
        Fotografo.objects.get_or_create(user=self.object)
        return url


class ClienteList(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "paginas/cliente_list.html"
    context_object_name = "objetos"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Cliente.objects.all()
        return Cliente.objects.filter(user=self.request.user)



class ClienteCreate(LoginRequiredMixin, CreateView):
    model = Cliente
    fields = ["nome", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("clientes")
    extra_context = {"titulo": "Novo cliente"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ClienteUpdate(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ["nome", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("clientes")
    extra_context = {"titulo": "Editar cliente"}

    def get_object(self, queryset=None):
        return get_object_or_404(Cliente, pk=self.kwargs["pk"])

class ClienteDelete(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = "paginas/confirm_delete.html"
    success_url = reverse_lazy("clientes")
    extra_context = {"titulo": "Excluir cliente"}

    def get_object(self, queryset=None):
        qs = Cliente.objects.all()
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            qs = qs.filter(user=self.request.user)
        return get_object_or_404(qs, pk=self.kwargs["pk"])



class FotografoList(LoginRequiredMixin, ListView):
    model = Fotografo
    template_name = "paginas/fotografo_list.html"
    context_object_name = "objetos"

    def get_queryset(self):
        return Fotografo.objects.filter(user=self.request.user)


class FotografoCreate(LoginRequiredMixin, CreateView):
    model = Fotografo
    fields = ["nome", "especialidade", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("fotografos")
    extra_context = {"titulo": "Novo fotógrafo"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FotografoUpdate(LoginRequiredMixin, UpdateView):
    model = Fotografo
    fields = ["nome", "especialidade", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("fotografos")
    extra_context = {"titulo": "Editar fotógrafo"}

    def get_object(self, queryset=None):
        return get_object_or_404(Fotografo, pk=self.kwargs["pk"], user=self.request.user)


class FotografoDelete(LoginRequiredMixin, DeleteView):
    model = Fotografo
    template_name = "paginas/confirm_delete.html"
    success_url = reverse_lazy("fotografos")
    extra_context = {"titulo": "Excluir fotógrafo"}

    def get_object(self, queryset=None):
        return get_object_or_404(Fotografo, pk=self.kwargs["pk"], user=self.request.user)


class EstudioList(UserOwnedQuerysetMixin, ListView):
    model = Estudio
    template_name = "paginas/estudio_list.html"
    context_object_name = "objetos"


class EstudioCreate(UserOwnedQuerysetMixin, CreateView):
    model = Estudio
    fields = ["nome", "endereco", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("estudios")
    extra_context = {"titulo": "Novo estúdio"}


class EstudioUpdate(UserOwnedQuerysetMixin, UpdateView):
    model = Estudio
    fields = ["nome", "endereco", "telefone"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("estudios")
    extra_context = {"titulo": "Editar estúdio"}

    def get_object(self, queryset=None):
        return get_object_or_404(
            Estudio,
            pk=self.kwargs["pk"],
            cadastrado_por=self.request.user,
        )


class EstudioDelete(UserOwnedQuerysetMixin, DeleteView):
    model = Estudio
    template_name = "paginas/confirm_delete.html"
    success_url = reverse_lazy("estudios")
    extra_context = {"titulo": "Excluir estúdio"}

    def get_object(self, queryset=None):
        return get_object_or_404(
            Estudio,
            pk=self.kwargs["pk"],
            cadastrado_por=self.request.user,
        )


class SessaoFotoList(UserOwnedQuerysetMixin, ListView):
    model = SessaoFoto
    template_name = "paginas/sessao_list.html"
    context_object_name = "objetos"


class SessaoFotoCreate(UserOwnedQuerysetMixin, CreateView):
    model = SessaoFoto
    fields = ["data", "horario", "duracao", "tipo", "valor", "finalizado", "cliente", "fotografo", "estudio"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("sessoes")
    extra_context = {"titulo": "Nova sessão"}

class SessaoFotoUpdate(UserOwnedQuerysetMixin, UpdateView):
    model = SessaoFoto
    fields = ["data", "horario", "duracao", "tipo", "valor", "finalizado", "cliente", "fotografo", "estudio"]
    template_name = "paginas/form.html"
    success_url = reverse_lazy("sessoes")
    extra_context = {"titulo": "Editar sessão"}

class SessaoFotoDelete(UserOwnedQuerysetMixin, DeleteView):
    model = SessaoFoto
    template_name = "paginas/confirm_delete.html"
    success_url = reverse_lazy("sessoes")
    extra_context = {"titulo": "Excluir sessão"}

    def get_object(self, queryset=None):
        return get_object_or_404(
            SessaoFoto,
            pk=self.kwargs["pk"],
            cadastrado_por=self.request.user,
        )
