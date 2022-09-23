from django.contrib import admin
from mptt.admin import MPTTModelAdmin

# Register your models here.
from project.models import Project, Task, Board, TaskHistory, Votes, Message

admin.site.register(Votes)


class BoardInline(admin.TabularInline):
    model = Board
    fields=('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        BoardInline
    ]
    list_display = ("id", "title", "description", "created_by")
    list_filter = ("title", "description",)
    search_fields = ("created_by__email", "created_by__username", "title")


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
