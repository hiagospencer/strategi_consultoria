from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class HeroiMarvel(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=1000)
    img = models.ImageField(upload_to='imagem')


    def __str__(self):
        return self.nome





class EquipeHeroi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=1000)


    def __str__(self):
        return self.nome

        