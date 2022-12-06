from django.test import TestCase, Client

from project.models import Project
from users.models import User


class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost:8000')
        self.user = User.objects.create_superuser(email='testadmin@admin.com', password='pass@123', is_active=True)
        self.project = Project.objects.create(title="test", description="testing description", created_by=self.user)

    def test_get_project(self):
        project_data = Project.objects.get(slug=self.project.slug)
        self.assertEqual(project_data.slug, self.project.slug)

    def test_non_login_listing_projects(self):
        response = self.client.get('/admin/projects/')
        self.assertFalse(response.status_code == 302, False)

    def test_listing_projects(self):
        self.client.force_login(self.user)
        response = self.client.get('/admin/projects/')
        self.assertEqual(response.status_code, 200)

    def test_delete_project(self):
        self.client.force_login(self.user)
        Project.objects.get(slug=self.project.slug).delete()
        self.assertFalse(Project.objects.filter(slug=self.project.slug).exists())
