import json

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import View

from common.custom_messages import message_dict
from home.views import BaseContextView
from project.models import Task, Message, Votes
from users.forms import RegisterUserForm, UpdateUserForm, LoginForm


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy("users:signin")
    template_name = "users/register.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)
        return redirect("home:home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.role = Group.objects.get_or_create(name='user')[0]
        obj.save()
        messages.success(
            self.request,
            message_dict.get('registration')
        )
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)


class EditProfileView(LoginRequiredMixin, BaseContextView, FormView):
    form_class = UpdateUserForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("home:home")

    def get_instace(self):
        return self.request.user

    def form_valid(self, form):
        instance = self.get_instace()
        instance.first_name = form.cleaned_data.get('first_name')
        instance.last_name = form.cleaned_data.get('last_name')
        instance.save()
        messages.success(self.request, "Saved Profile")
        return super(EditProfileView, self).form_valid(form)

    def form_invalid(self, form):
        return super(EditProfileView, self).form_invalid(form)


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_message = 'Login successfully'
    success_url = reverse_lazy("home:home")

    def get_success_url(self):
        if self.get_redirect_url():
            self.success_url = self.get_redirect_url()
            return self.success_url

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return reverse_lazy("home:home")
        return super(CustomLoginView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        return super(CustomLoginView, self).form_invalid(form)


class RemoveAccountView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        self.request.user.delete()
        messages.success(self.request, message_dict.get('logout'))
        return redirect("home:home")


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:signin")

    def get(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, message_dict.get('logout'))
        return redirect("home:home")


class MyItemView(LoginRequiredMixin, BaseContextView, TemplateView):
    template_name = 'users/my_items.html'

    def get_context_data(self, **kwargs):
        context = super(MyItemView, self).get_context_data()
        context['commented_tasks'] = []
        context['items'] = json.dumps(
            list(Task.objects.filter(created_by=self.request.user).annotate(num_votes=Count('user_task')).values(
                'num_votes', 'id', 'name', 'project__title', 'type__name', 'project__slug', 'created', 'slug')),
            indent=4, sort_keys=True,
            default=str)
        context['comments'] = json.dumps(
            list(Message.objects.filter(user=self.request.user).annotate(num_votes=Count('task__user_task')).values('text','num_votes','task__name', 'created', 'task__slug','task__project__title','task__type__name'
                                                                       ,'id')),
            indent=4, sort_keys=True, default=str)
        context['votes'] = json.dumps(list(
            Votes.objects.filter(user=self.request.user).annotate(num_votes=Count('task')).values('task__name', 'task__project__title',
                                                                'task__is_subscribed','created','num_votes',
                                                                'task__slug', 'task__project__slug','task__type__name')), indent=4,
            sort_keys=True, default=str)

        return context
