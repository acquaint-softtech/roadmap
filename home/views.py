from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from custom_admin.models import GeneralSettings
from project.forms import TaskCreateForm
from project.models import Task


class BaseContextView(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseContextView, self).get_context_data()
        context['task_form'] = TaskCreateForm()
        context['projects'] = Task.objects.filter(created_by=self.request.user, project__isnull=False).values(
            'project__title', 'project__slug').distinct('project') if self.request.user.is_authenticated else []
        context['general_settings'] = GeneralSettings.objects.first()
        return context


class HomeView(BaseContextView, TemplateView):
    template_name = 'home/home.html'
