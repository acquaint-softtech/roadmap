import datetime
import json

from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import View

from common.custom_messages import message_dict
from home.views import BaseContextView
from project.models import Task, Message, Votes
from users.forms import RegisterUserForm, UpdateUserForm, LoginForm
from users.models import UserSetting, User
from users.token import account_activation_token


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class EmailVerify(LoginRequiredMixin, BaseContextView, TemplateView):
    template_name = 'users/email_verify.html'

    def post(self, request, *args, **kwargs):
        get_user_activate_account_link(request, request.user)
        return redirect('users:email_verify')


class RegisterView(BaseContextView, CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy("users:signing")
    template_name = "users/register.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)
        return redirect("home:home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.is_active = False
        obj.save()
        messages.success(
            self.request,
            message_dict.get('registration')
        )

        get_user_activate_account_link(self.request, obj)
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)


def get_user_activate_account_link(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activation link has been sent to your email id'
    message = render_to_string('users/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(mail_subject, message)
    return True


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_verified_at = datetime.datetime.now()
            user.save()
            login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return redirect('home:home')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('users:signing')


class EditProfileView(LoginRequiredMixin, BaseContextView, FormView):
    form_class = UpdateUserForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("users:profile")

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data()
        notification_obj = UserSetting.objects.filter(user=self.request.user).first()
        context['notification'] = notification_obj
        context['option'] = notification_obj.page_par_sizes
        return context

    def get_instace(self):
        return self.request.user

    def form_valid(self, form):
        notification = self.get_context_data()['notification']
        instance = self.get_instace()
        instance.first_name = form.data.get('first_name')
        instance.mention_name = form.data.get('mention_name') if form.data.get('mention_name') else form.data.get(
            'first_name').lower().replace(' ', '-')
        instance.email = form.data.get('email')
        notification.mention_notifications = True if form.data.get('mention_notifications') == 'on' else False
        notification.reply_notifications = True if form.data.get('reply_notifications') == 'on' else False
        notification.page_par_sizes = sorted(self.request.POST['selected'].split(','), key=int)

        instance.save()
        notification.save()
        messages.success(self.request, "Saved Profile")
        return super(EditProfileView, self).form_valid(form)

    def form_invalid(self, form):
        return super(EditProfileView, self).form_invalid(form)


class CustomLoginView(BaseContextView, LoginView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_message = 'Login successfully'
    success_url = reverse_lazy("home:home")

    def get_success_url(self):
        if self.get_redirect_url() != '':
            self.success_url = self.get_redirect_url()
            return self.success_url
        else:
            return self.success_url

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember')
        login(self.request, form.get_user(),backend='users.auth_backend.CustomAuthBackend')
        if remember_me != 'on':
            self.request.session.set_expiry(0)
        return HttpResponseRedirect(self.get_success_url())

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
    login_url = reverse_lazy("users:signing")

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
            list(Message.objects.filter(user=self.request.user).annotate(num_votes=Count('task__user_task')).values(
                'text', 'num_votes', 'task__name', 'created', 'task__slug', 'task__project__title', 'task__type__name'
                , 'id')),
            indent=4, sort_keys=True, default=str)
        context['votes'] = json.dumps(list(
            Votes.objects.filter(user=self.request.user).annotate(num_votes=Count('task')).values('task__name',
                                                                                                  'task__project__title',
                                                                                                  'task__is_subscribed',
                                                                                                  'created',
                                                                                                  'num_votes',
                                                                                                  'task__slug',
                                                                                                  'task__project__slug',
                                                                                                  'task__type__name')),
            indent=4,
            sort_keys=True, default=str)

        context['recent_mentions'] = json.dumps(
            list(Message.objects.filter(mention_user=self.request.user).values('task__name', 'text', 'created',
                                                                               'task__slug')),
            indent=4,
            sort_keys=True, default=str)
        context['options'] = self.request.user.settings.page_par_sizes
        return context


class MyPasswordResetView(BaseContextView, PasswordResetView):
    template_name = 'users/reset_password.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:reset_password')

    def form_invalid(self, form):
        return super(MyPasswordResetView, self).form_invalid(form)


class MyPasswordResetConfirmView(BaseContextView, PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('home:home')

    def form_invalid(self, form):
        return super(MyPasswordResetConfirmView, self).form_invalid(form)
