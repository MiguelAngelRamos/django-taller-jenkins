# tasks/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Task

class TaskAPITestCase(APITestCase):
    """
    Suite de pruebas para validar los endpoints CRUD de la entidad Task.
    Sigue el patrón AAA (Arrange, Act, Assert).
    """

    def setUp(self):
        # Arrange: Preparamos el estado inicial de la base de datos para cada test
        self.task_1 = Task.objects.create(
            title="Aprender Docker", 
            description="Entender volúmenes y redes"
        )
        self.list_url = '/api/v1/tasks/'
        self.detail_url = f'/api/v1/tasks/{self.task_1.id}/'

    def test_crear_tarea(self):
        # Arrange
        data = {
            "title": "Configurar Jenkins",
            "description": "Crear pipeline declarativo"
        }
        
        # Act
        response = self.client.post(self.list_url, data, format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(id=response.data['id']).title, "Configurar Jenkins")

    def test_listar_tareas(self):
        # Act
        response = self.client.get(self.list_url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificamos que al menos viene la tarea que creamos en el setUp
        self.assertEqual(len(response.data), 1) 
        self.assertEqual(response.data[0]['title'], self.task_1.title)

    def test_obtener_tarea_por_id(self):
        # Act
        response = self.client.get(self.detail_url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task_1.title)

    def test_actualizar_tarea(self):
        # Arrange
        data = {
            "title": "Aprender Docker Profundamente",
            "completed": True
        }
        
        # Act (Usamos PUT para actualización completa, o PATCH para parcial)
        response = self.client.put(self.detail_url, data, format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_1.refresh_from_db() # Refrescamos la instancia local con los datos de la BD
        self.assertTrue(self.task_1.completed)
        self.assertEqual(self.task_1.title, "Aprender Docker Profundamente")

    def test_eliminar_tarea(self):
        # Act
        response = self.client.delete(self.detail_url)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)