from django.db.models import Count
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from custom_admin.models import GeneralSetting
from project.forms import TaskCreateForm
from project.models import Project, Message, Task


class BaseContextView(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseContextView, self).get_context_data()
        context['task_form'] = TaskCreateForm()
        context['projects'] = Project.objects.select_related('created_by').values('title', 'slug', 'is_private',
                                                                                  'created_by__email').order_by(
            '-created')
        context['general_settings'] = GeneralSetting.objects.first()
        return context


class HomeView(BaseContextView, TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        context['recent_comments'] = Message.objects.select_related('task').values('task__name', 'task__slug',
                                                                                   'text').order_by('-id')[0:10]
        context['recent_items'] = Task.objects.select_related('project', 'type').annotate(
            num_votes=Count('user_task'))
        return context
