from django.shortcuts import render
from rest_framework import viewsets, filters, status
from .models import Autor, Livro
from .serializers import AutorSerializer, LivroSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
  
    def create(self, request, *args, **kwargs):
        if Autor.objects.filter(nome=request.data.get('nome')).exists():
            return Response({"detail": "Autor já existe."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'autor__nome']

    @action(detail=True, methods=['patch'])
    def atualizar_titulo(self, request, pk=None):
        livro = self.get_object()
        novo_titulo = request.data.get('titulo')
        
        if not novo_titulo:
            return Response({"detail": "Título não pode ser vazio."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        livro.titulo = novo_titulo
        livro.save()
        return Response({'status': 'Título atualizado!'})

    @action(detail=False, methods=['get'])
    def publicados_recente(self, request):
        um_ano_atras = timezone.now() - timedelta(days=365)
        livros_recentes = Livro.objects.filter(data_publicacao__gte=um_ano_atras)
        serializer = self.get_serializer(livros_recentes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        total_livros = Livro.objects.count()
        livros_por_autor = Autor.objects.annotate(qtd_livros=Count('livros')).values('nome', 'qtd_livros')
        
        return Response({
            'total_livros': total_livros,
            'livros_por_autor': list(livros_por_autor)
        })
