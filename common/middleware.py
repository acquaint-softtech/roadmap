from django.core.cache import cache
from django.db.models import Count

from custom_admin.models import GeneralSetting
from project.models import Project, Task, Message, Vote
from users.models import User


class CustomCacheMiddleware(object):
    """
    This class is used to get data from cache.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.user_data = cache.get('user_data')
        self.project_data = cache.get('project_data')
        self.task_data = cache.get('task_data')
        self.message_data = cache.get('message_data')
        self.inbox_data = cache.get('inbox_data')
        self.vote_data = cache.get('vote_data')
        self.admin_task_data = cache.get('admin_task_data')
        self.settings = cache.get('settings')

        if any(data is None for data in
               [self.user_data, self.project_data, self.task_data, self.message_data, self.inbox_data, self.vote_data,
                self.admin_task_data, self.settings]):
            self.set_cache_value()

    def set_cache_value(self):
        if not self.user_data:
            self.user_data = User.objects.values('id', 'first_name', 'role__name', 'email', 'date_joined').order_by(
                '-date_joined')
            cache.set('user_data', self.user_data)

        if not self.project_data:
            self.project_data = Project.objects.annotate(
                board_count=Count('board_project')).values('id', 'title', 'created',
                                                           'is_private', 'slug', 'board_count').order_by('-created')
            cache.set('project_data', self.project_data)

        if not self.task_data:
            self.task_data = Task.objects.filter(project__isnull=False).values('id', 'name', 'project__title',
                                                                               'type__name',
                                                                               'created_by__email', 'created',
                                                                               'is_pinned',
                                                                               'slug', 'created_by__id',
                                                                               'project__slug').order_by('-created')
            cache.set('task_data', self.task_data)

        if not self.message_data:
            self.message_data = Message.objects.values('id', 'text', 'task__name', 'user__email',
                                                       'created', 'task__slug', 'user__id').order_by('-created')
            cache.set('message_data', self.message_data)

        if not self.inbox_data:
            self.inbox_data = Task.objects.filter(project__isnull=True).annotate(
                comment_count=Count('message_task')).values(
                'id', 'name', 'created_by__email',
                'created', 'slug', 'comment_count', 'created_by__id').order_by('-created')

            cache.set('inbox_data', self.inbox_data)

        if not self.vote_data:
            self.vote_data = Vote.objects.values('id', 'user__email', 'task__name', 'task__is_subscribed', 'created',
                                                 'user__id', 'task__slug').order_by('-created')
            cache.set('vote_data', self.vote_data)

        if not self.admin_task_data:
            self.admin_task_data = Task.objects.select_related('project', 'type').annotate(
                num_task_histories=Count('task_history'))
            cache.set('admin_task_data', self.admin_task_data)

        if not self.settings:
            self.settings = GeneralSetting.objects.first()
            cache.set('settings', self.settings)

        return True

    def __call__(self, request):
        response = self.get_response(request)
        return response
