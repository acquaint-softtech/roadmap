import json

from django.contrib import messages
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.views.generic.base import ContextMixin, View

from project.admin import BoardAdminFormSet
from project.forms import ProjectCreateForm, AdminTaskForm, AdminCommentForm, BoardForm, AdminUserForm
from project.models import Project, Task, Message, TaskHistory, Board, Votes
from users.models import User
from users.views import LoginRequiredMixin


class AdminContextView(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(AdminContextView, self).get_context_data()
        context['inbox_count'] = Task.objects.filter(project__isnull=True).count()
        return context


class AdminHomeView(LoginRequiredMixin,AdminContextView, TemplateView):
    template_name = 'custom_admin/admin_home.html'


class ProjectList(AdminContextView, LoginRequiredMixin, ListView):
    model = Project
    template_name = 'custom_admin/projects.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        projects = super(ProjectList, self).get_queryset(*args, **kwargs)
        projects = projects.filter(created_by=self.request.user).order_by('-id')
        return projects


class ProjectCreateView(AdminContextView, LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    success_url = reverse_lazy("custom_admin:projects")
    template_name = "custom_admin/new_project.html"

    def get_context_data(self, **kwargs):

        BoardFormSet = inlineformset_factory(
            Project, Board, form=BoardForm, formset=BoardAdminFormSet,
            fields=['name', 'detail', 'is_visible', 'is_block_votes', 'is_user_delete', 'is_block_comments'], extra=5,
            can_delete=True
        )

        formset = BoardFormSet(initial=[
            {'name': 'Under review'}, {'name': 'Planned'}, {'name': 'In progress'}, {'name': 'Live'}, {'name': 'Closed'}
        ])

        data = super(ProjectCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['boards'] = BoardFormSet(self.request.POST)
        else:
            data['boards'] = formset
        return data

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        context = self.get_context_data()
        boards = context['boards']
        if boards.is_valid():
            boards.instance = obj
            boards.save()

        messages.success(
            self.request,
            "Project created successfully."
        )
        return super(ProjectCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ProjectCreateView, self).form_invalid(form)


class ProjectUpdateView(AdminContextView, LoginRequiredMixin, UpdateView):
    model = Project
    success_url = reverse_lazy("custom_admin:projects")
    template_name = "custom_admin/edit_project.html"
    fields = ["title", "description", "url", "is_private"]
    success_message = 'Project updated successfully'

    BoardFormSet = inlineformset_factory(
        Project, Board, form=BoardForm,
        fields=['name', 'detail', 'is_visible', 'is_block_votes', 'is_user_delete', 'is_block_comments'], extra=0,
        can_delete=True
    )

    def get_context_data(self, **kwargs):
        data = super(ProjectUpdateView, self).get_context_data(**kwargs)
        data['boards'] = self.BoardFormSet(instance=self.object)
        return data

    def post(self, request, *args, **kwargs):
        formset = self.BoardFormSet(request.POST, instance=self.get_object())
        if self.get_form().is_valid() and formset.is_valid():
            self.get_form().save()
            formset.save()
        return super().post(request, *args, **kwargs)


class ProjectDeleteView(AdminContextView, LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("custom_admin:projects")
    template_name = "custom_admin/project_confirm_delete.html"
    success_message = 'Project deleted successfully'


class InboxList(AdminContextView, LoginRequiredMixin, ListView):
    model = Task
    template_name = 'custom_admin/inbox.html'
    context_object_name = 'inboxes'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        inboxes = super(InboxList, self).get_queryset(*args, **kwargs)
        inboxes = inboxes.filter(project__isnull=True).order_by('-id')
        return inboxes


class AdminTaskList(AdminContextView, LoginRequiredMixin, ListView):
    model = Task
    template_name = 'custom_admin/tasks.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        tasks = super(AdminTaskList, self).get_queryset(*args, **kwargs)
        tasks = tasks.filter(project__isnull=False).order_by('-id')
        return tasks


class TaskCreateView(AdminContextView, LoginRequiredMixin, CreateView):
    form_class = AdminTaskForm
    success_url = reverse_lazy("custom_admin:projects")
    template_name = "custom_admin/add_task.html"

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['project'] = self.request.GET.get('project')
        return kwargs

    def form_valid(self, form):
        messages.success(
            self.request,
            "Task created successfully."
        )
        return super(TaskCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(TaskCreateView, self).form_invalid(form)


class TaskUpdateView(AdminContextView, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = AdminTaskForm
    success_url = reverse_lazy("custom_admin:tasks")
    template_name = "custom_admin/edit_task.html"
    success_message = 'Task updated successfully'

    def get_form_kwargs(self):
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs['project'] = self.request.GET.get('project')
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(*args, **kwargs)
        context['comments'] = Message.objects.select_related('task').filter(
            task__slug=self.kwargs.get('slug')).order_by('id')
        return context


class TaskDeleteView(AdminContextView, LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("custom_admin:tasks")
    template_name = "custom_admin/task_confirm_delete.html"
    success_message = 'Task deleted successfully'


class CommentsList(AdminContextView, LoginRequiredMixin, ListView):
    model = Message
    template_name = 'custom_admin/comments.html'
    context_object_name = 'comments'
    ordering = ['-id']
    paginate_by = 10


class CommentCreateView(AdminContextView, LoginRequiredMixin, CreateView):
    form_class = AdminCommentForm
    success_url = reverse_lazy("custom_admin:comments")
    template_name = "custom_admin/new_comment.html"

    def form_valid(self, form):
        messages.success(
            self.request,
            "Comment created successfully."
        )
        return super(CommentCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CommentCreateView, self).form_invalid(form)


class CommentUpdateView(AdminContextView, LoginRequiredMixin, UpdateView):
    model = Message
    form_class = AdminCommentForm
    success_url = reverse_lazy("custom_admin:comments")
    template_name = "custom_admin/edit_comment.html"
    success_message = 'Comment updated successfully'


class CommentDeleteView(AdminContextView, LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("custom_admin:comments")
    template_name = "custom_admin/comment_confirm_delete.html"
    success_message = 'Comment deleted successfully'


class ChangeTaskStatus(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        task_slug = request.POST['task_slug']
        task_obj = Task.objects.get(slug=task_slug)
        task_obj.type_id = int(request.POST['task_status'])
        task_obj.save()
        TaskHistory.objects.create(task=task_obj, action_by=request.user,
                                   note=f'moved item to board {task_obj.type.name}')
        return redirect('project:task_detail', slug=task_slug)


class AdminUserList(AdminContextView, LoginRequiredMixin, ListView):
    model = User
    template_name = 'custom_admin/users.html'
    context_object_name = 'users'
    paginate_by = 10
    ordering = ['-id']


class UserCreateView(AdminContextView, LoginRequiredMixin, CreateView):
    form_class = AdminUserForm
    success_url = reverse_lazy("custom_admin:users")
    template_name = "custom_admin/add_user.html"

    def form_invalid(self, form):
        return super(UserCreateView, self).form_invalid(form)


class UserUpdateView(AdminContextView, LoginRequiredMixin, UpdateView):
    model = User
    form_class = AdminUserForm
    success_url = reverse_lazy("custom_admin:users")
    template_name = "custom_admin/edit_user.html"
    success_message = 'User updated successfully'


class UserDeleteView(AdminContextView, LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("custom_admin:users")
    template_name = "custom_admin/user_confirm_delete.html"
    success_message = 'User deleted successfully'


class AdminVoteList(AdminContextView, LoginRequiredMixin, ListView):
    model = Votes
    template_name = 'custom_admin/votes.html'
    context_object_name = 'votes'
    paginate_by = 10
    ordering = ['-id']


class ChangeVote(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        vote, created = Votes.objects.get_or_create(user=request.user, task_id=data.get('task_id'))
        if not created:
            vote.delete()
        return JsonResponse({"message": "success", "created": created})


class ChangeTaskSubscription(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        task_data = Task.objects.filter(id=int(data.get('task_id'))).first()
        task_data.is_subscribed = not (task_data.is_subscribed)
        task_data.save()
        return JsonResponse({"message": "success"})


class AdminThemeView(LoginRequiredMixin,AdminContextView, TemplateView):
    template_name = 'custom_admin/theme.html'


class AdminSettingsView(LoginRequiredMixin,AdminContextView, TemplateView):
    template_name = 'custom_admin/settings.html'


class AdminSystemView(LoginRequiredMixin, AdminContextView, TemplateView):
    template_name = 'custom_admin/settings.html'
