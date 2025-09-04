from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nome = models.CharField(max_length=100, null=True)
    telefone = models.CharField(max_length=20, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Fotografo(models.Model):
    nome = models.CharField(max_length=100, null=True)
    especialidade = models.CharField(max_length=100, null=True)
    telefone = models.CharField(max_length=20, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

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
        return f"{self.cadastrado_por.username} - {self.data} {self.horario}"

 





