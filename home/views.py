from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from custom_admin.models import GeneralSettings
from project.forms import TaskCreateForm
from project.models import Project


class BaseContextView(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseContextView, self).get_context_data()
        context['task_form'] = TaskCreateForm()
        context['projects'] = Project.objects.select_related('created_by').values('title', 'slug', 'is_private',
                                                                                  'created_by__email').order_by(
            '-created')
        context['general_settings'] = GeneralSettings.objects.first()
        return context


class HomeView(BaseContextView, TemplateView):
    template_name = 'home/home.html'
