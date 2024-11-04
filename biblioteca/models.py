from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Autor(models.Model):
    nome = models.CharField(max_length=180)
    
    def __str__(self):
        return self.nome
    
class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, related_name='livros', on_delete=models.CASCADE)
    data_publicacao = models.DateField()
    numero_paginas = models.IntegerField()
    
    def __str__(self):
        return self.titulo
    
    def clean(self):
        # Verifica se o autor está definido
        if not self.autor:
            raise ValidationError({'autor': 'Um livro deve ter um autor associado.'})

    def save(self, *args, **kwargs):
        # Chama o método clean para garantir a validação
        self.clean()
        super().save(*args, **kwargs)
