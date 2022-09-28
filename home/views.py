from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from project.forms import TaskCreateForm
from project.models import Task


class BaseContextView(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseContextView, self).get_context_data()
        context['task_form'] = TaskCreateForm()
        context['projects'] = Task.objects.filter(created_by=self.request.user, project__isnull=False).values(
            'project__title', 'project__slug').distinct('project') if self.request.user.is_authenticated else []
        return context


class HomeView(BaseContextView, TemplateView):
    template_name = 'home/home.html'


class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'home/dashboard.html'


class MyItemView(LoginRequiredMixin,BaseContextView, TemplateView):
    template_name = 'users/my_items.html'