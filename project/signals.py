from django.core.cache import cache
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from project.models import TaskHistory, Task, TaskNotification, Project, Message, Votes
from users.models import User


@receiver(post_save, sender=Task)
def save_task_history(sender, created, instance, **kwargs):
    if created:
        get_admin_users = list(User.objects.filter(is_superuser=True).values_list('id', flat=True).distinct())
        TaskHistory.objects.create(task=instance, action_by=instance.created_by, note='created the item')
        history_data = []
        for user in get_admin_users:
            if instance.created_by.id != user:
                history_data.append(TaskNotification(task=instance, assign_by_id=user))
        TaskNotification.objects.bulk_create(history_data)

    cache.delete('task_data')
    cache.delete('admin_task_data')


@receiver(post_delete, sender=Project)
def save_project(sender, created, instance, **kwargs):
    cache.delete('project_data')


@receiver(post_delete, sender=Message)
def save_comments(sender, created, instance, **kwargs):
    cache.delete('message_data')


@receiver(post_delete, sender=Votes)
def save_votes(sender, created, instance, **kwargs):
    cache.delete('vote_data')
