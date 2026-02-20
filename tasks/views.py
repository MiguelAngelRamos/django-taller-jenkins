# tasks/views.py
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    Controlador que provee las acciones estándar de CRUD para el modelo Task.
    """
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer