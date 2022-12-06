from django.test import TestCase, Client

from project.models import Project, Task
from users.models import User


class TaskTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost:8000')
        self.user = User.objects.create_superuser(email='test1admin@admin.com', password='pass@123', is_active=True)
        self.project = Project.objects.create(title="test", description="testing description", created_by=self.user)
        self.task = Task.objects.create(name="test_task", project=self.project, created_by=self.user,
                                        description='testing description')

    def test_get_task(self):
        task_data = Task.objects.get(slug=self.task.slug)
        self.assertEqual(task_data.slug, self.task.slug)

    def test_non_login_listing_tasks(self):
        response = self.client.get('/admin/items/')
        self.assertFalse(response.status_code == 302, False)

    def test_listing_tasks(self):
        self.client.force_login(self.user)
        response = self.client.get('/admin/items/')
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        self.client.force_login(self.user)
        Task.objects.get(slug=self.task.slug).delete()
        self.assertFalse(Task.objects.filter(slug=self.task.slug).exists())
