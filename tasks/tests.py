from urllib import response
from django.test import TestCase, RequestFactory
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.apiviews import TaskViewSet
from tasks.views import CreateTaskView, DeleteTaskView, UpdateTaskView
from .models import Task


class TestAllTaskView(TestCase):
    def test_authenticated(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login?next=/')


class TestDetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="bruce_wayne", email="bruce@wayne.org", password="i_am_batman")
        self.task = Task.objects.create(
            title='testing', description='testing description', user=self.user)

    def test_working(self):
        response = self.client.get(f"/{self.task.id}/")
        self.assertEqual(response.status_code, 200)


class TestCreateTaskView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@…', password='top_secret')

    def test_create(self):
        request_content = {
            'title': 'testing1',
            'description': 'testing1 description',
        }

        request = self.factory.post(
            reverse('create_task'), data=request_content)
        request.user = self.user
        response = CreateTaskView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestUpdateTaskView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@…', password='top_secret')
        self.task = Task.objects.create(
            title='task update test', description='task update test description', user=self.user)

    def test_update(self):
        request_content = {
            'title': 'task updated',
            'description': 'task updated description',
        }
        request = self.factory.post(
            reverse('update_task', kwargs={'pk': self.task.id}), data=request_content)
        response = UpdateTaskView.as_view()(request, pk=self.task.id)
        self.assertEqual(response.status_code, 200)


class TestDeleteView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@…', password='top_secret')
        self.task = Task.objects.create(
            title='task update test', description='task update test description', user=self.user)
        self.task.save()

    def test_delete(self):
        request = self.factory.post(
            reverse('delete_task', kwargs={'pk': self.task.id}))
        response = DeleteTaskView.as_view()(request, pk=self.task.id)
        self.assertEqual(response.status_code, 302)


class TestApiTaskViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testuser@.com', password='top_secret')
        self.client.post(
            f'/accounts/login/', data={'username': 'testuser', 'password': 'top_secret'})

    def test_create_task(self):
        request_content = {
            'title': 'testing222',
            'description': 'testing222 description',
            'status': 'PENDING',
            'user': self.user
        }

        response = self.client.post('/api/task/', data=request_content)
        self.assertEqual(response.status_code, 201)

    def test_update_task(self):
        request_content = {
            'title': 'updated task',
            'description': 'testing updated',
            'status': 'PENDING'
        }
        self.client.post('/api/task/', data={'title': 'testing222', 'description': 'testing222 description', 'status': 'PENDING', 'user': self.user})
        task = Task.objects.last()
        response = self.client.put(f'/api/task/{task.id}/', data=request_content)
        self.assertEqual(response.status_code, 200)
