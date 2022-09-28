# Create your views here.
from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView

from home.views import BaseContextView
from project.forms import MessageForm
from project.models import Project, Task, Message, TaskHistory
from users.views import LoginRequiredMixin

print(connection.queries)


class ProjectList(BaseContextView, LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'

    def get_queryset(self, *args, **kwargs):
        projects = super(ProjectList, self).get_queryset(*args, **kwargs)
        projects = projects.filter(created_by=self.request.user)
        return projects


class TaskList(BaseContextView, LoginRequiredMixin, ListView):
    model = Task
    template_name = 'projects/new_project_detail.html'
    context_object_name = 'tasks'

    def get_queryset(self, *args, **kwargs):
        tasks = []
        task_data = super(TaskList, self).get_queryset(*args, **kwargs)
        task_data = task_data.select_related('type').filter(project__slug=self.kwargs.get('slug')).values('name',
                                                                                                          'created',
                                                                                                          'type__name',
                                                                                                          'slug',
                                                                                                          'is_pinned')
        tasks.append({
            'Review': task_data.filter(type__name='Review'),
            'General': task_data.filter(type__name='General'),
            'In-progress': task_data.filter(type__name='In-progress'),
            'In-discussion': task_data.filter(type__name='In-discussion'),
            'closed': task_data.filter(type__name='closed'),
        })
        return tasks


class TaskDetailView(BaseContextView, LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'projects/task_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TaskDetailView,
                        self).get_context_data(*args, **kwargs)
        context["message_form"] = MessageForm()
        context['message_data'] = Message.objects.select_related('task', 'user').filter(
            task__slug=self.kwargs.get('slug'))
        context['history_data'] = TaskHistory.objects.select_related('task', 'action_by').filter(
            task__slug=self.kwargs.get('slug'))
        print(context['history_data'], "context['history_data']")
        return context


class SaveTaskView(BaseContextView, LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        description = request.POST.get('description')
        Task.objects.create(name=name, description=description, created_by=request.user)
        messages.success(request, 'Task Created successfully.')
        return redirect('home:home')


class SaveCommentView(BaseContextView, LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        text_data = request.POST.get('text')
        task_id = int(request.POST.get('task_id'))
        task_slug = request.POST.get('task_slug')
        message_id = request.POST.get('message_id')
        parent_id = request.POST.get('parent_id')

        if not text_data:
            return redirect('project:task_detail', slug=task_slug)

        if message_id:
            Message.objects.filter(id=message_id).update(text=text_data)
        else:
            Message.objects.create(text=text_data, task_id=task_id, user=request.user, parent_id=parent_id)

        return redirect('project:task_detail', slug=task_slug)
