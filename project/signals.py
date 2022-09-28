from django.db.models.signals import post_save
from django.dispatch import receiver

from project.models import TaskHistory, Task, Project, Board

task_status = ['In-discussion', 'In-progress', 'General', 'Review', 'Live', 'Closed']


@receiver(post_save, sender=Task)
def save_task_history(sender, created, instance, **kwargs):
    if created:
        TaskHistory.objects.create(task=instance, action_by=instance.created_by, note='created the item')


# @receiver(post_save, sender=Project)
# def save_task_history(sender, created, instance, **kwargs):
#     if created:
#         types = []
#         for status in task_status:
#             types.append(Board(name=status, project=instance))
#         Board.objects.bulk_create(types)
