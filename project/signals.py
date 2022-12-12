from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from project.models import TaskHistory, Task, TaskNotification, Project, Message, Vote
from users.models import User
from django.core.mail import EmailMessage


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

        notify_user_data = cache.get('settings').send_notifications_to
        for data in notify_user_data:
            # we can add custom email template for body part
            email = EmailMessage(data['name'], f'New item {instance.name} created', to=[data['email']])
            email.send()

    cache.delete('task_data')
    cache.delete('admin_task_data')


@receiver(post_delete, sender=Project)
def delete_project(sender, instance, *args, **kwargs):
    cache.delete('project_data')


@receiver(post_delete, sender=Message)
def delete_comments(sender, instance, *args, **kwargs):
    cache.delete('message_data')


@receiver(post_delete, sender=Vote)
def delete_votes(sender, instance, *args, **kwargs):
    cache.delete('vote_data')
