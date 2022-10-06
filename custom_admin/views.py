import json

from django.contrib import messages
from django.db.models import Count
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView
from django.views.generic.base import ContextMixin, View

from project.admin import BoardAdminFormSet
from project.forms import ProjectCreateForm, AdminTaskForm, AdminCommentForm, BoardForm, AdminUserForm
from project.models import Project, Task, Message, TaskHistory, Board, Votes, TaskNotification
from users.models import User
from users.views import LoginRequiredMixin


class AdminContextView(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(AdminContextView, self).get_context_data()
        context['inbox_count'] = Task.objects.filter(project__isnull=True).count()
        task_notifications = TaskNotification.objects.select_related('task', 'created_by').filter(
            is_read=False, is_deleted=False, assign_by=self.request.user).values('task__name', 'created', 'task__slug',
                                                                                 'task__created_by__id',
                                                                                 'task__created_by__email').order_by(
            '-created')
        context['task_notifications'] = json.dumps(list(task_notifications), indent=4, sort_keys=True, default=str)
        return context


class AdminHomeView(LoginRequiredMixin, AdminContextView, TemplateView):
    template_name = 'custom_admin/admin_home.html'

    def get_context_data(self, **kwargs):
        context = super(AdminHomeView, self).get_context_data()
        task_data = Task.objects.select_related('project', 'type').annotate(num_task_histories=Count('task_history'))
        context['latest_items'] = task_data.order_by('-created')[0:5]
        context['popular_items'] = task_data.order_by('-num_task_histories')[0:5]
        return context


class ProjectList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/projects.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectList, self).get_context_data(*args, **kwargs)
        project_data = Project.objects.annotate(
            board_count=Count('category_project')).values('id', 'title', 'created',
                                                          'is_private', 'slug', 'board_count')
        context['projects'] = json.dumps(list(project_data), indent=4, sort_keys=True, default=str)
        return context


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


class InboxList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/inbox.html'

    def get_context_data(self, *args, **kwargs):
        context = super(InboxList, self).get_context_data(*args, **kwargs)
        inbox_data = Task.objects.filter(project__isnull=True).annotate(comment_count=Count('message_task')).values(
            'id', 'name', 'created_by__email',
            'created', 'slug', 'comment_count')
        context['inbox'] = json.dumps(list(inbox_data), indent=4, sort_keys=True, default=str)
        return context


class AdminTaskList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/tasks.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdminTaskList, self).get_context_data(*args, **kwargs)
        task_data = Task.objects.filter(project__isnull=False).values('id', 'name', 'project__title', 'type__name',
                                                                      'created_by__email', 'created', 'is_pinned',
                                                                      'slug')
        context['tasks'] = json.dumps(list(task_data), indent=4, sort_keys=True, default=str)
        return context


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


class CommentsList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/comments.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CommentsList, self).get_context_data(*args, **kwargs)
        message_data = Message.objects.values('id', 'text', 'task__name', 'user__email',
                                              'created')
        context['messages'] = json.dumps(list(message_data), indent=4, sort_keys=True, default=str)
        return context


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


class AdminUserList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/users.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdminUserList, self).get_context_data(*args, **kwargs)
        user_data = User.objects.values('id', 'first_name', 'role__name', 'email', 'date_joined')
        context['users'] = json.dumps(list(user_data), indent=4, sort_keys=True, default=str)
        return context


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


class AdminVoteList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/votes.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdminVoteList, self).get_context_data(*args, **kwargs)
        vote_data = Votes.objects.values('id', 'user__email', 'task__name', 'task__is_subscribed', 'created')
        context['votes'] = json.dumps(list(vote_data), indent=4, sort_keys=True, default=str)
        return context


class ChangeVote(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        vote, created = Votes.objects.get_or_create(user=request.user, task_id=data.get('task_id'))
        if not created:
            vote.task.is_subscribed = False
            vote.task.save()
            vote.delete()
        else:
            vote.task.is_subscribed = True
            vote.task.save()

        return JsonResponse({"message": "success", "created": created})


class ChangeTaskSubscription(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        task_data = Task.objects.filter(id=int(data.get('task_id'))).first()
        task_data.is_subscribed = not (task_data.is_subscribed)
        task_data.save()
        return JsonResponse(
            {"message": "success", "btn_status": 'Unsubscribe' if task_data.is_subscribed else 'Subscribe'})


class AdminThemeView(LoginRequiredMixin, AdminContextView, TemplateView):
    template_name = 'custom_admin/theme.html'


class AdminSettingsView(LoginRequiredMixin, AdminContextView, TemplateView):
    template_name = 'custom_admin/settings.html'


class AdminSystemView(LoginRequiredMixin, AdminContextView, TemplateView):
    template_name = 'custom_admin/settings.html'


class ProjectWiseBoard(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        boards = Board.objects.filter(project_id=int(data['project_id'])).values('id', 'name')
        data = json.dumps(list(boards), sort_keys=True, default=str)
        return JsonResponse(
            {"message": "success", "boards": data})


class NotificationView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        TaskNotification.objects.filter(is_read=False,assign_by = request.user).update(is_read=True) if data[
                                                                                   'type'] == 'read' else TaskNotification.objects.filter(
            is_deleted=False,assign_by = request.user).update(is_deleted=True)
        return JsonResponse({"message": "success"})
