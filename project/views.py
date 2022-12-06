# Create your views here.
import json
import re

from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView

from home.views import BaseContextView
from project.forms import MessageForm
from project.models import Project, Task, Message, TaskHistory, Board, Vote
from users.models import User
from users.views import LoginRequiredMixin


class ProjectList(BaseContextView, LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'

    def get_queryset(self, *args, **kwargs):
        projects = super(ProjectList, self).get_queryset(*args, **kwargs)
        projects = projects.filter(created_by=self.request.user)
        return projects


class TaskList(BaseContextView, ListView):
    model = Task
    template_name = 'projects/project_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TaskList, self).get_context_data(*args, **kwargs)
        tasks = []
        task_data = Task.objects.select_related('type').annotate(num_votes=Count('user_task')).filter(
            project__slug=self.kwargs.get('slug')).values('name',
                                                          'created',
                                                          'type__name',
                                                          'slug',
                                                          'is_pinned', 'num_votes')

        boards = Board.objects.filter(project__slug=self.kwargs.get('slug')).values_list('name', flat=True).distinct()

        for board in boards:
            tasks.append({
                board: task_data.filter(type__name=board)
            })

        context['tasks'] = tasks
        context['project_name'] = Project.objects.filter(slug=self.kwargs.get('slug')).first()
        return context


class TaskDetailView(BaseContextView, DetailView):
    model = Task
    template_name = 'projects/task_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TaskDetailView, self).get_context_data(*args, **kwargs)
        context["message_form"] = MessageForm()
        context["boards"] = Board.objects.filter(project=self.object.project).values('name', 'id')
        context['votes'] = list(
            Vote.objects.select_related('task', 'user').filter(task=self.object).values_list('user__email',
                                                                                              flat=True).distinct())
        context['message_data'] = Message.objects.select_related('task', 'user').filter(
            task__slug=self.kwargs.get('slug'))
        context['history_data'] = TaskHistory.objects.select_related('task', 'action_by').filter(
            task__slug=self.kwargs.get('slug')).order_by('-created')[0:10]
        context['vote_data'] = Vote.objects.filter(user=self.request.user,
                                                    task=self.object).first() if self.request.user.is_authenticated \
            else False

        users = list(User.objects.exclude(
            email=self.request.user.email if self.request.user.is_authenticated else '').values_list('mention_name',
                                                                                                     flat=True))
        context['users'] = json.dumps(users, indent=4, sort_keys=True)

        return context


class SaveTaskView(BaseContextView, LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        name = data.get('task_title')
        description = data.get('task_description')
        Task.objects.create(name=name, description=description, created_by=request.user)
        messages.success(request, 'Item created successfully.')
        return JsonResponse({"message": "success"})


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
            obj = Message.objects.filter(id=message_id).first()
            obj.text = text_data
            obj.save()
        else:
            obj = Message.objects.create(text=text_data, task_id=task_id, user=request.user, parent_id=parent_id)

        if '@' in text_data:
            mention_users = re.findall("@([a-zA-Z0-9]{1,15})", re.sub(r'<.*?>', '', text_data))
            user_obj = User.objects.filter(mention_name__in=mention_users)
            for user in user_obj:
                obj.mention_user.add(user)

            obj.save()

        return redirect('project:task_detail', slug=task_slug)
