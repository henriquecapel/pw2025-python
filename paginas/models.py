from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nome = models.CharField(max_length=100, null=True)
    telefone = models.CharField(max_length=20, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} ({self.telefone})"

class Fotografo(models.Model):
    nome = models.CharField(max_length=100, null=True)
    especialidade = models.CharField(max_length=100, null=True)
    telefone = models.CharField(max_length=20, null=True)
    foto_perfil = models.URLField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"

class Sessao(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    tipo = models.CharField(max_length=50)
    duracao = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=7,decimal_places=2)
    finalizado = models.BooleanField(default=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fotografo = models.ForeignKey(Fotografo, on_delete=models.PROTECT)
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sessão: {self.tipo} | Cliente: {self.cliente.nome} | Fotógrafo: {self.fotografo.nome} | {self.data} {self.horario}"

# crie um portfolio para o fotografo de fotos com os links das fotos e não uploads
class Portfolio(models.Model):
    fotografo = models.ForeignKey(Fotografo, on_delete=models.CASCADE)
    foto_url = models.URLField()
    descricao = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Portfolio de {self.fotografo.nome}: {self.foto_url}"
 





