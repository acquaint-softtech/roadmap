import uuid

from ckeditor.fields import RichTextField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from common.models import TimeStampModel
from project.utils import unique_slugify
from users.models import User


class Project(TimeStampModel):
    project_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    description = RichTextField()
    is_private = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='user',
                                   on_delete=models.CASCADE, null=True, blank=True)

    def save(self, **kwargs):
        unique_slugify(self, self.title)
        super(Project, self).save(**kwargs)

    def __str__(self):
        return self.title


class Board(TimeStampModel):
    name = models.CharField(max_length=255)
    is_visible = models.BooleanField(default=True)
    is_block_votes = models.BooleanField(default=False)
    is_user_delete = models.BooleanField(default=False)
    is_block_comments = models.BooleanField(default=False)
    detail = models.TextField(null=True,blank=True)
    project = models.ForeignKey(Project, related_name='category_project',
                                on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Task(TimeStampModel):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, related_name='assign_user',
                                   on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, related_name='task_project',
                                on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey(Board, related_name='task_type',
                             on_delete=models.CASCADE, null=True, blank=True)
    description = RichTextField(null=True)
    is_pinned = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    def save(self, **kwargs):
        unique_slugify(self, self.name)
        super(Task, self).save(**kwargs)

    def __str__(self):
        return self.name


class Message(TimeStampModel, MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='message_user',
                             on_delete=models.CASCADE, null=True, blank=True)

    task = models.ForeignKey(Task, related_name='message_task',
                             on_delete=models.CASCADE, null=True, blank=True)
    text = RichTextField(null=True)

    class MPTTMeta:
        level_attr = 'mptt_level'


class TaskHistory(TimeStampModel):
    action_by = models.ForeignKey(User, related_name='action_by',
                                  on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, related_name='task_history',
                             on_delete=models.CASCADE, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)


class Votes(TimeStampModel):
    user = models.ForeignKey(User, related_name='vote_by',
                             on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, related_name='user_task',
                             on_delete=models.CASCADE, null=True, blank=True)
