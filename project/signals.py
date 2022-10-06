from django.db.models.signals import post_save
from django.dispatch import receiver

from project.models import TaskHistory, Task, TaskNotification
from users.models import User

get_admin_users = list(User.objects.filter(is_superuser=True).values_list('id', flat=True).distinct())


@receiver(post_save, sender=Task)
def save_task_history(sender, created, instance, **kwargs):
    if created:
        TaskHistory.objects.create(task=instance, action_by=instance.created_by, note='created the item')
        history_data = []
        for user in get_admin_users:
            if instance.created_by.id != user:
                history_data.append(TaskNotification(task=instance, assign_by_id=user))
        TaskNotification.objects.bulk_create(history_data)
