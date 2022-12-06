from django.contrib import admin
from django.forms.models import BaseInlineFormSet, ModelForm
from mptt.admin import MPTTModelAdmin

from project.models import Project, Task, Board, TaskHistory, Vote, Message, TaskNotification


class BoardAdminFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs and kwargs['instance'].pk is None:
            kwargs['initial'] = [
                {'name': 'Under review'}, {'name': 'Planned'}, {'name': 'In progress'}, {'name': 'Live'},
                {'name': 'Closed'}
            ]
        super(BoardAdminFormSet, self).__init__(*args, **kwargs)


class BoardModelForm(ModelForm):

    def has_changed(self, *args, **kwargs):
        if self.instance.pk is None:
            return True
        return super(BoardModelForm, self).has_changed(*args, **kwargs)


class BoardInline(admin.TabularInline):
    model = Board
    fields = ('name', 'detail', 'is_visible', 'is_block_votes', 'is_user_delete', 'is_block_comments')
    extra = 5
    formset = BoardAdminFormSet
    form = BoardModelForm

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return self.extra


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (BoardInline,)
    list_display = ("id", "title", "description", "created_by")
    search_fields = ("created_by__email", "created_by__username", "title")


class TaskHistoryInline(admin.TabularInline):
    model = TaskHistory
    can_delete = False
    verbose_name_plural = 'task_history'
    fk_name = 'task'
    extra = 1


class TaskNotificationInline(admin.TabularInline):
    model = TaskNotification
    can_delete = False
    verbose_name_plural = 'task_notification'
    fk_name = 'task'
    extra = 1


class VoteInline(admin.TabularInline):
    model = Vote
    can_delete = False
    verbose_name_plural = 'vote'
    fk_name = 'task'
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by", "created", "project")
    inlines = (TaskHistoryInline, TaskNotificationInline, VoteInline,)
    search_fields = ("name", "created_by__email")


@admin.register(Message)
class MessageAdmin(MPTTModelAdmin):
    list_display = ("id", "user", "task", "text", "created")
    search_fields = ("user", "task")


@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "action_by", "task", "note", "created")
    search_fields = ("action_by", "task")


@admin.register(TaskNotification)
class TaskNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "assign_by", "is_read", "created")
    search_fields = ("assign_by", "task")


@admin.register(Vote)
class VotesAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "subscribed")
    search_fields = ("task", "user")
