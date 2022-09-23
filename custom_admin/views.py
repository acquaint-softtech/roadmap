from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.views.generic.base import ContextMixin

from project.forms import ProjectCreateForm, AdminTaskForm, AdminCommentForm
from project.models import Project, Task, Message
from users.views import LoginRequiredMixin


class AdminContextView(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(AdminContextView, self).get_context_data()
        context['inbox_count'] = Task.objects.filter(project__isnull=True).count()
        return context


class AdminHomeView(AdminContextView, TemplateView):
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


class AdminTaskList(AdminContextView, LoginRequiredMixin, ListView):
    model = Task
    template_name = 'custom_admin/tasks.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        tasks = super(AdminTaskList, self).get_queryset(*args, **kwargs)
        tasks = tasks.filter(project__isnull=False).order_by('-id')
        return tasks


class ProjectCreateView(AdminContextView, LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    success_url = reverse_lazy("custom_admin:projects")
    template_name = "custom_admin/new_project.html"

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        messages.success(
            self.request,
            "Project created successfully."
        )
        return super(ProjectCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ProjectCreateView, self).form_invalid(form)


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


class ProjectUpdateView(AdminContextView, LoginRequiredMixin, UpdateView):
    model = Project
    success_url = reverse_lazy("custom_admin:projects")
    template_name = "custom_admin/edit_project.html"
    fields = ["title", "description", "url", "is_private"]
    success_message = 'Project updated successfully'


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
