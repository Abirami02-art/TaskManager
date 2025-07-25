from django.test import TestCase, Client
from django.urls import reverse
from .models import TaskManager

class TaskManagerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = TaskManager.objects.create(name="Test Task", description="Test Description")

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_add_task_view_get(self):
        response = self.client.get(reverse('add_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_form.html')

    def test_add_task_view_post(self):
        response = self.client.post(reverse('add_task'), {
            'name': 'New Task',
            'description': 'New Task Description'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(TaskManager.objects.filter(name='New Task').exists())

    def test_list_task_view(self):
        response = self.client.get(reverse('list_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_list.html')
        self.assertContains(response, self.task.name)

    def test_update_task_view_get(self):
        response = self.client.get(reverse('update_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_update.html')

    def test_update_task_view_post(self):
        response = self.client.post(reverse('update_task', args=[self.task.id]), {
            'name': 'Updated Task',
            'description': 'Updated Description'
        })
        self.assertEqual(response.status_code, 302)
        updated = TaskManager.objects.get(id=self.task.id)
        self.assertEqual(updated.name, 'Updated Task')

    def test_delete_task_view(self):
        response = self.client.get(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskManager.objects.filter(id=self.task.id).exists())
