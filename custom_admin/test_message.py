from django.test import TestCase, Client

from project.models import Project, Task, Message
from users.models import User


class MessageTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost:8000')
        self.user = User.objects.create_superuser(email='test1admin@admin.com', password='pass@123', is_active=True)
        self.project = Project.objects.create(title="test", description="testing description", created_by=self.user)
        self.task = Task.objects.create(name="test_task", project=self.project, created_by=self.user,
                                        description='testing description')
        self.message = Message.objects.create(task=self.task, text="testing description", user=self.user)

    def test_get_message(self):
        message_data = Message.objects.get(id=self.message.id)
        self.assertEqual(message_data.id, self.message.id)

    def test_non_login_listing_messages(self):
        response = self.client.get('/admin/comments/')
        self.assertFalse(response.status_code == 302, False)

    def test_listing_messages(self):
        self.client.force_login(self.user)
        response = self.client.get('/admin/comments/')
        self.assertEqual(response.status_code, 200)

    def test_delete_message(self):
        self.client.force_login(self.user)
        Message.objects.get(id=self.message.id).delete()
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())
