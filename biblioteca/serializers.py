from rest_framework import serializers
from .models import Autor, Livro

class LivroSerializer(serializers.ModelSerializer):
  class Meta:
    model = Livro
    fields = ['id', 'titulo', 'autor', 'data_publicacao', 'numero_paginas']
    
class AutorSerializer(serializers.ModelSerializer):
  livros = LivroSerializer(many=True, read_only=True)
  
  class Meta:
    model = Autor
    fields = ['id', 'nome', 'livros']