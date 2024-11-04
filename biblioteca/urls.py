from rest_framework.routers import DefaultRouter
from .views import AutorViewSet, LivroViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'autores', AutorViewSet)
router.register(r'livros', LivroViewSet)

urlpatterns =[
  path('', include(router.urls))
]