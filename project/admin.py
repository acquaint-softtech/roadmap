from django.contrib import admin
from django.forms.models import BaseInlineFormSet, ModelForm
from mptt.admin import MPTTModelAdmin

# Register your models here.
from project.models import Project, Task, Board, TaskHistory, Votes, Message

admin.site.register(Votes)


class BoardAdminFormSet(BaseInlineFormSet):

    def __init__(self,*args, **kwargs):
        if 'instance' in kwargs and  kwargs['instance'].pk is None:
            kwargs['initial'] = [
                {'name': 'Under review'}, {'name': 'Planned'}, {'name': 'In progress'}, {'name': 'Live'}, {'name': 'Closed'}
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
    inlines = [
        BoardInline
    ]
    list_display = ("id", "title", "description", "created_by")
    list_filter = ("title", "description",)
    search_fields = ("created_by__email", "created_by__username", "title")


admin.site.register(Board)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by", "created", "project")
    search_fields = ("name", "created_by__email")


@admin.register(Message)
class MessageAdmin(MPTTModelAdmin):
    list_display = ("id", "user", "task", "text", "created")
    search_fields = ("user", "task")


@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "action_by", "task", "note", "created")
    search_fields = ("action_by", "task")