from django.test import TestCase, Client

from users.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost:8000')
        self.user = User.objects.create_user(email='testing@gmail.com', password='testing@123')

    def test_get_user(self):
        user_data = User.objects.get(id=self.user.id)
        self.assertEqual(user_data.id, self.user.id)

    def test_user_is_superuser(self):
        self.assertFalse(self.user.is_superuser, False)

    def test_user_is_active(self):
        self.assertTrue(self.user.is_active, True)

    def test_user_login(self):
        self.assertTrue(self.client.login(email=self.user.email, password=self.user.password), True)

    def test_user_wrong_password(self):
        self.assertFalse(self.user.check_password('testing'), False)

