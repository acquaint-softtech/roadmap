from django.test import TestCase, Client

from project.models import Project, Board
from users.models import User


class BoardTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost:8000')
        self.user = User.objects.create_superuser(email='test1admin@admin.com', password='pass@123', is_active=True)
        self.project = Project.objects.create(title="test", description="testing description", created_by=self.user)
        self.board = Board.objects.create(name='testing_board', detail='testing details', project=self.project)

    def test_get_board(self):
        board_data = Board.objects.get(id=self.board.id)
        self.assertEqual(board_data.id, self.board.id)

    def test_unique_board(self):
        board_count = Board.objects.filter(project=self.project, name='testing_board').count()
        self.assertFalse(board_count is not 0, False)

    def test_delete_board(self):
        self.client.force_login(self.user)
        Board.objects.get(id=self.board.id).delete()
        self.assertFalse(Board.objects.filter(id=self.board.id).exists())
