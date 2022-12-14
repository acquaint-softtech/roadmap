import json
import os
import platform

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Count
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, FormView
from django.views.generic.base import ContextMixin, View

from common.custom_messages import message_dict
from common.middleware import CustomCacheMiddleware
from custom_admin.forms import GeneralNotificationForm, ThemeForm
from custom_admin.models import GeneralSetting
from project.admin import BoardAdminFormSet
from project.forms import ProjectCreateForm, AdminTaskForm, AdminCommentForm, BoardForm, AdminUserForm, VoteForm
from project.models import Project, Task, Message, TaskHistory, Board, Vote, TaskNotification
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
            '-created') if self.request.user.is_authenticated else []
        context['task_notifications'] = json.dumps(list(task_notifications), indent=4, sort_keys=True, default=str)
        context['general_settings'] = cache.get('settings')
        context['tasks'] = json.dumps(list(Task.objects.values('name', 'slug')), indent=4, sort_keys=True, default=str)
        return context


class AdminHomeView(LoginRequiredMixin, AdminContextView, TemplateView):
    template_name = 'custom_admin/admin_home.html'

    def get_context_data(self, **kwargs):
        context = super(AdminHomeView, self).get_context_data()
        cache_data = CustomCacheMiddleware(object)
        context['latest_items'] = cache_data.admin_task_data.order_by('-created')[
                                  0:5] if cache_data.admin_task_data else []
        context['popular_items'] = cache_data.admin_task_data.order_by('-num_task_histories')[
                                   0:5] if cache_data.admin_task_data else []
        return context


class ProjectList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/projects.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectList, self).get_context_data(*args, **kwargs)
        cache_data = CustomCacheMiddleware(object)
        context['projects'] = json.dumps(list(cache_data.project_data), indent=4, sort_keys=True, default=str)
        context['data'] = {'app_name': 'Project', 'type': 'List', 'listing_url': reverse_lazy("custom_admin:projects")}
        return context


class ProjectCreateView(AdminContextView, LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    success_url = reverse_lazy("custom_admin:projects")
    template_name = "custom_admin/new_project.html"

    cache_data = CustomCacheMiddleware(object)
    general_settings = cache_data.settings

    BoardFormSet = inlineformset_factory(
        Project, Board, form=BoardForm, formset=BoardAdminFormSet,
        fields=['name', 'detail', 'is_visible', 'is_block_votes', 'is_user_delete', 'is_block_comments'],
        extra=len(general_settings.default_boards if general_settings and general_settings.center_default_board else []),
        can_delete=True
    )

    formset = BoardFormSet(
        initial=[{'name': data} for data in
                 general_settings.default_boards] if general_settings and general_settings.center_default_board else [])

    def get_context_data(self, **kwargs):
        data = AdminContextView.get_context_data(self)
        data['data'] = {'app_name': 'Project', 'type': 'Create', 'listing_url': reverse_lazy("custom_admin:projects")}
        data['boards'] = self.formset
        return data

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        board_formset = self.BoardFormSet(self.request.POST)
        project_form = self.form_class(data=request.POST, user=request.user)
        if project_form.is_valid() and board_formset.is_valid():
            return self.form_valid(board_formset, project_form)
        return self.form_invalid(self.form_class)

    def form_valid(self, formset, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        formset_obj = formset.save(commit=False)
        for data in formset_obj:
            data.project = obj
            data.save()
        self.success_url = reverse_lazy("custom_admin:projects") if 'submit' in form.data else reverse_lazy(
            "custom_admin:new_project")
        messages.success(self.request, message_dict.get('new_record'))
        return super(ProjectCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ProjectCreateView, self).form_invalid(form)


class ProjectUpdateView(AdminContextView, LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse_lazy("custom_admin:projects")
    template_name = "custom_admin/edit_project.html"
    success_message = 'Project updated successfully'

    BoardFormSet = inlineformset_factory(
        Project, Board, form=BoardForm,
        fields=['name', 'detail', 'is_visible', 'is_block_votes', 'is_user_delete', 'is_block_comments'], extra=0,
        can_delete=True
    )

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(ProjectUpdateView, self).get_context_data(**kwargs)
        data['data'] = {'app_name': 'Project', 'type': 'Edit', 'listing_url': reverse_lazy("custom_admin:projects")}
        data['boards'] = self.BoardFormSet(instance=self.object)
        return data

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        board_formset = self.BoardFormSet(self.request.POST, instance=self.get_object())
        project_form = self.form_class(data=request.POST, user=request.user, instance=self.get_object())
        if project_form.is_valid() and board_formset.is_valid():
            return self.form_valid(board_formset, project_form)
        return self.form_invalid(self.form_class)

    def form_valid(self, formset, form):
        form.save()
        formset.save()
        messages.success(self.request, message_dict.get('edit_record'))
        return super(ProjectUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ProjectUpdateView, self).form_invalid(form)


class ProjectDeleteView(AdminContextView, LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("custom_admin:projects")
    success_message = 'Project deleted successfully'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class InboxList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/inbox.html'

    def get_context_data(self, *args, **kwargs):
        context = super(InboxList, self).get_context_data(*args, **kwargs)
        cache_data = CustomCacheMiddleware(object)
        context['inbox'] = json.dumps(list(cache_data.inbox_data), indent=4, sort_keys=True, default=str)
        context['data'] = {'app_name': 'Inbox', 'type': 'List', 'listing_url': reverse_lazy("custom_admin:inbox")}
        return context


class AdminTaskList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/tasks.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdminTaskList, self).get_context_data(*args, **kwargs)
        cache_data = CustomCacheMiddleware(object)
        context['tasks'] = json.dumps(list(cache_data.task_data), indent=4, sort_keys=True, default=str)
        context['data'] = {'app_name': 'Item', 'type': 'List', 'listing_url': reverse_lazy("custom_admin:tasks")}
        return context


class TaskCreateView(AdminContextView, LoginRequiredMixin, CreateView):
    form_class = AdminTaskForm
    success_url = reverse_lazy("custom_admin:items")
    template_name = "custom_admin/add_task.html"

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['project'] = self.request.GET.get('project')
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(TaskCreateView, self).get_context_data(*args, **kwargs)
        context['data'] = {'app_name': 'Item', 'type': 'Create', 'listing_url': reverse_lazy("custom_admin:tasks")}
        return context

    def form_valid(self, form):
        self.success_url = reverse_lazy("custom_admin:tasks") if 'submit' in form.data else reverse_lazy(
            "custom_admin:new_task")
        messages.success(
            self.request,
            message_dict.get("new_record")
        )
        return super(TaskCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(TaskCreateView, self).form_invalid(form)


class TaskUpdateView(AdminContextView, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = AdminTaskForm
    vote_form_class = VoteForm
    success_url = reverse_lazy("custom_admin:tasks")
    template_name = "custom_admin/edit_task.html"
    success_message = 'Task updated successfully'

    def get_form_kwargs(self):
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs['project'] = self.request.GET.get('project')
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(*args, **kwargs)
        context['data'] = {'app_name': 'Item', 'type': 'Edit', 'listing_url': reverse_lazy("custom_admin:tasks")}

        context['comments'] = json.dumps(
            list(Message.objects.filter(task=self.object).values('text', 'task__name', 'created', 'task__slug', 'id',
                                                                 'user__email').order_by('-created')),
            indent=4, sort_keys=True, default=str)
        context['votes'] = json.dumps(list(
            Vote.objects.filter(task=self.object).values('task__is_subscribed', 'id',
                                                         'task__slug', 'task__project__slug', 'user__email',
                                                         'subscribed', 'user__id',
                                                         'created').order_by('-created')),
            indent=4,
            sort_keys=True, default=str)

        context['task_histories'] = json.dumps(list(
            TaskHistory.objects.filter(task=self.object).values('note', 'created', 'action_by__email').order_by(
                '-created')), indent=4, sort_keys=True, default=str)

        context['vote_form'] = self.vote_form_class
        return context

    def form_valid(self, form):
        obj = form.save()
        if obj.project_id and obj.type_id:
            Vote.objects.get_or_create(task=obj, user=obj.created_by)
        messages.success(
            self.request,
            message_dict.get("edit_record")
        )
        return super(TaskUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(TaskUpdateView, self).form_invalid(form)


class TaskDeleteView(AdminContextView, LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("custom_admin:tasks")
    success_message = 'Task deleted successfully'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CommentsList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/comments.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CommentsList, self).get_context_data(*args, **kwargs)
        cache_data = CustomCacheMiddleware(object)
        context['message_data'] = json.dumps(list(cache_data.message_data), indent=4, sort_keys=True, default=str)
        context['data'] = {'app_name': 'Comments', 'type': 'List', 'listing_url': reverse_lazy("custom_admin:comments")}
        return context


class CommentCreateView(AdminContextView, LoginRequiredMixin, CreateView):
    form_class = AdminCommentForm
    success_url = reverse_lazy("custom_admin:comments")
    template_name = "custom_admin/new_comment.html"

    def get_context_data(self, **kwargs):
        context = AdminContextView.get_context_data(self)
        context['data'] = {'app_name': 'Comment', 'type': 'Create',
                           'listing_url': reverse_lazy("custom_admin:comments")}
        return context

    def form_valid(self, form):
        self.success_url = reverse_lazy("custom_admin:comments") if 'submit' in form.data else reverse_lazy(
            "custom_admin:new_comment")
        messages.success(
            self.request,
            message_dict.get("new_record")
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

    def get_context_data(self, **kwargs):
        context = AdminContextView.get_context_data(self)
        context['data'] = {'app_name': 'Comment', 'type': 'Edit', 'listing_url': reverse_lazy("custom_admin:comments")}
        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            message_dict.get("edit_record")
        )
        return super(CommentUpdateView, self).form_valid(form)


class CommentDeleteView(AdminContextView, LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("custom_admin:comments")
    success_message = 'Comment deleted successfully'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ChangeTaskStatus(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        task_slug = request.POST['task_slug']
        task_obj = Task.objects.get(slug=task_slug)
        task_obj.type_id = int(request.POST['task_status'])
        task_obj.save()
        TaskHistory.objects.create(task=task_obj, action_by=request.user,
                                   note=f'moved item to board {task_obj.type.name}')

        messages.success(request, f"Successfully moved the item to board {task_obj.type.name}")
        return redirect('project:task_detail', slug=task_slug)


class AdminUserList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/users.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdminUserList, self).get_context_data(*args, **kwargs)
        cache_data = CustomCacheMiddleware(object)
        context['users'] = json.dumps(list(cache_data.user_data), indent=4, sort_keys=True, default=str)
        context['data'] = {'app_name': 'Users', 'type': 'List', 'listing_url': reverse_lazy("custom_admin:users")}
        return context


class UserCreateView(AdminContextView, LoginRequiredMixin, CreateView):
    form_class = AdminUserForm
    success_url = reverse_lazy("custom_admin:users")
    template_name = "custom_admin/add_user.html"

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['data'] = {'app_name': 'User', 'type': 'Create', 'listing_url': reverse_lazy("custom_admin:users")}
        return context

    def form_valid(self, form):
        self.success_url = reverse_lazy("custom_admin:users") if 'submit' in form.data else reverse_lazy(
            "custom_admin:new_user")
        messages.success(self.request, message_dict.get('new_record'))
        return super(UserCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UserCreateView, self).form_invalid(form)


class UserUpdateView(AdminContextView, LoginRequiredMixin, UpdateView):
    model = User
    form_class = AdminUserForm
    template_name = "custom_admin/edit_user.html"
    success_message = 'User updated successfully'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('custom_admin:update_user', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['items'] = json.dumps(
            list(Task.objects.filter(created_by=self.object).annotate(num_votes=Count('user_task')).values(
                'num_votes', 'id', 'name', 'project__title', 'type__name', 'project__slug', 'created', 'slug')),
            indent=4, sort_keys=True,
            default=str)
        context['comments'] = json.dumps(
            list(Message.objects.filter(user=self.object).values('text', 'task__name', 'created', 'task__slug', 'id')),
            indent=4, sort_keys=True, default=str)
        context['votes'] = json.dumps(list(
            Vote.objects.filter(user=self.object).values('task__name', 'task__project__title', 'task__is_subscribed',
                                                         'task__slug', 'task__project__slug', 'id')), indent=4,
            sort_keys=True, default=str)
        context['data'] = {'app_name': 'User', 'type': 'Edit', 'listing_url': reverse_lazy("custom_admin:users")}
        return context

    def form_valid(self, form):
        messages.success(self.request, message_dict.get('edit_record'))
        return super(UserUpdateView, self).form_valid(form)


class UserDeleteView(AdminContextView, LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("custom_admin:users")
    success_message = 'User deleted successfully'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AdminVoteList(TemplateView, AdminContextView, LoginRequiredMixin):
    template_name = 'custom_admin/votes.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdminVoteList, self).get_context_data(*args, **kwargs)
        cache_data = CustomCacheMiddleware(object)
        context['votes'] = json.dumps(list(cache_data.vote_data), indent=4, sort_keys=True, default=str)
        context['data'] = {'app_name': 'Votes', 'type': 'List', 'listing_url': reverse_lazy("custom_admin:votes")}
        return context


class ChangeVote(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        vote, created = Vote.objects.get_or_create(user=request.user, task_id=data.get('task_id'))
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
        task_data.is_subscribed = not task_data.is_subscribed
        task_data.save()
        return JsonResponse(
            {"message": "success", "btn_status": 'Unsubscribe' if task_data.is_subscribed else 'Subscribe'})


class AdminThemeView(LoginRequiredMixin, AdminContextView, FormView):
    template_name = 'custom_admin/theme.html'
    form_class = ThemeForm
    success_url = reverse_lazy('custom_admin:theme')

    def get_context_data(self, **kwargs):
        context = AdminContextView.get_context_data(self)
        data = GeneralSetting.objects.first()
        form = ThemeForm(instance=data)
        context['form'] = form
        return context

    def form_valid(self, form):
        form = ThemeForm(instance=GeneralSetting.objects.first(), data=self.request.POST, files=self.request.FILES)
        form.save()
        messages.success(self.request, message_dict.get('edit_record'))
        return super(AdminThemeView, self).form_valid(form)

    def form_invalid(self, form):
        return super(AdminThemeView, self).form_invalid(form)


class AdminSettingsView(LoginRequiredMixin, AdminContextView, View):
    template_name = 'custom_admin/settings.html'
    form_class = GeneralNotificationForm
    success_url = reverse_lazy('custom_admin:settings')

    def get(self, request, *args, **kwargs):
        context = AdminContextView.get_context_data(self)
        data = GeneralSetting.objects.first()
        form = GeneralNotificationForm(instance=data)
        context['total_og_img'] = len(
            os.listdir(os.path.join(settings.MEDIA_ROOT, 'project_og_img'))) if os.path.exists(
            os.path.join(settings.MEDIA_ROOT, 'project_og_img')) else 0
        context['form'] = form
        context['board_data'] = data.default_boards
        context['data'] = data
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = GeneralNotificationForm(instance=GeneralSetting.objects.first(), data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.default_boards = request.POST.get('board_data').split(',')
            obj.send_notifications_to = json.loads(request.POST.get('notify_user'))
            obj.save()
        messages.success(self.request, message_dict.get('edit_record'))
        return redirect(self.success_url)


class AdminSystemView(LoginRequiredMixin, AdminContextView, TemplateView):
    template_name = 'custom_admin/system.html'

    def get_context_data(self, **kwargs):
        context = super(AdminSystemView, self).get_context_data()
        context['python_version'] = platform.python_version()
        return context


class ProjectWiseBoard(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        boards = Board.objects.filter(project_id=int(data['project_id'])).values('id', 'name') if data[
            'project_id'] else []
        data = json.dumps(list(boards), sort_keys=True, default=str)
        return JsonResponse(
            {"message": "success", "boards": data})


class NotificationView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        TaskNotification.objects.filter(is_read=False, assign_by=request.user).update(is_read=True) if data[
                                                                                                           'type'] == 'read' else TaskNotification.objects.filter(
            is_deleted=False, assign_by=request.user).update(is_deleted=True)
        return JsonResponse({"message": "success"})


class VoteDeleteView(AdminContextView, LoginRequiredMixin, DeleteView):
    model = Vote
    success_url = reverse_lazy("custom_admin:votes")
    success_message = 'Vote deleted successfully'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SaveTaskVote(AdminContextView, LoginRequiredMixin, View):
    form = VoteForm

    @staticmethod
    def get_redirect_url(self, task_slug):
        return redirect("custom_admin:update_task", slug=task_slug)

    def post(self, request, *args, **kwargs):

        task_slug = request.POST['task_slug']

        if not request.POST['vote_id']:
            form_data = self.form(data=request.POST)
            if form_data.is_valid():
                vote = form_data.save(commit=False)
                vote.task_id = int(request.POST['task_id'])
                vote.save()
        else:
            Vote.objects.filter(id=int(request.POST['vote_id'])).update(user_id=int(request.POST['user']),
                                                                        subscribed=True if 'subscribed' in
                                                                                           request.POST else False)

        return self.get_redirect_url(self, task_slug)


class RemoveOGImage(AdminContextView, LoginRequiredMixin, View):
    success_url = reverse_lazy('custom_admin:settings')

    def post(self, request, *args, **kwargs):

        if 'og_img_name' in request.POST:
            file_name = request.POST['og_img_name']
            redirect_path = request.POST['redirect_url']
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, "project_og_img", file_name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, "project_og_img", file_name))
            return redirect(redirect_path)

        else:
            for file in os.listdir(os.path.join(settings.MEDIA_ROOT, "project_og_img")):
                os.remove(os.path.join(settings.MEDIA_ROOT, "project_og_img", file))
            return redirect(self.success_url)
