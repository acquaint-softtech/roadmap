from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError

from project.models import Project, Task, Message, Board, Vote
from users.models import User


class ProjectCreateForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Project
        fields = (
            "title",
            "description",
            "url",
            "is_private"
        )


    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs[
            'class'] = 'block w-full rounded-lg border-none px-3 py-2 shadow-sm ring-1 ring-inset transition ' \
                       'duration-75 focus:ring-2 focus:ring-inset focus:ring-primary-500 disabled:opacity-70 ' \
                       'sm:py-2.5 sm:text-sm dark:bg-gray-700 dark:text-white dark:focus:ring-primary-500 ' \
                       'ring-gray-300 dark:ring-gray-600 '
        self.fields['url'].widget.attrs[
            'class'] = 'block w-full rounded-lg border-none px-3 py-2 shadow-sm ring-1 ring-inset transition ' \
                       'duration-75 focus:ring-2 focus:ring-inset focus:ring-primary-500 disabled:opacity-70 ' \
                       'sm:py-2.5 sm:text-sm dark:bg-gray-700 dark:text-white dark:focus:ring-primary-500 ' \
                       'ring-gray-300 dark:ring-gray-600'
        self.fields['is_private'].widget.attrs[
            'class'] = 'filament-forms-toggle-component relative inline-flex border-2 border-transparent shrink-0 h-6 ' \
                       'w-11 rounded-full cursor-pointer transition-colors ease-in-out duration-200 ' \
                       'focus:outline-none disabled:opacity-70 disabled:cursor-not-allowed ' \
                       'disabled:pointer-events-none bg-gray-200 dark:bg-white/10 '
        self.fields["title"].error_messages[
            "required"
        ] = "Please enter project title."
        self.fields["url"].error_messages[
            "required"
        ] = "Please enter project url."
        self.fields["description"].error_messages[
            "required"
        ] = "Please enter project description."

    def clean_title(self):
        title = self.cleaned_data['title']
        if Project.objects.exclude(id=self.instance.id).filter(title=title, created_by=self.user).exists():
            raise forms.ValidationError("Project already exits.")
        return title


class BoardForm(forms.ModelForm):
    sort_item = forms.ChoiceField(choices=(('Popular', 'Popular'), ('Latest', 'Latest')), required=True)

    class Meta:
        model = Board
        exclude = ('created', 'modified',)

    def __init__(self, *args, **kwargs):
        super(BoardForm, self).__init__(*args, **kwargs)
        self.fields['sort_item'].empty_label = 'Select an option'
        self.fields['name'].widget.attrs[
            'class'] = 'block w-full rounded-lg border-none px-3 py-2 shadow-sm ring-1 ring-inset transition ' \
                       'duration-75 focus:ring-2 focus:ring-inset focus:ring-primary-500 disabled:opacity-70 ' \
                       'sm:py-2.5 sm:text-sm dark:bg-gray-700 dark:text-white dark:focus:ring-primary-500 ' \
                       'ring-gray-300 dark:ring-gray-600 '
        self.fields['is_visible'].widget.attrs[
            'class'] = 'filament-forms-toggle-component relative inline-flex border-2 border-transparent shrink-0 h-6 ' \
                       'w-11 rounded-full cursor-pointer transition-colors ease-in-out duration-200 ' \
                       'focus:outline-none disabled:opacity-70 disabled:cursor-not-allowed ' \
                       'disabled:pointer-events-none bg-gray-200 dark:bg-white/10 '
        self.fields['is_block_votes'].widget.attrs[
            'class'] = 'filament-forms-toggle-component relative inline-flex border-2 border-transparent shrink-0 h-6 ' \
                       'w-11 rounded-full cursor-pointer transition-colors ease-in-out duration-200 ' \
                       'focus:outline-none disabled:opacity-70 disabled:cursor-not-allowed ' \
                       'disabled:pointer-events-none bg-gray-200 dark:bg-white/10 '
        self.fields['is_user_delete'].widget.attrs[
            'class'] = 'filament-forms-toggle-component relative inline-flex border-2 border-transparent shrink-0 h-6 ' \
                       'w-11 rounded-full cursor-pointer transition-colors ease-in-out duration-200 ' \
                       'focus:outline-none disabled:opacity-70 disabled:cursor-not-allowed ' \
                       'disabled:pointer-events-none bg-gray-200 dark:bg-white/10 '
        self.fields['is_block_comments'].widget.attrs[
            'class'] = 'filament-forms-toggle-component relative inline-flex border-2 border-transparent shrink-0 h-6 ' \
                       'w-11 rounded-full cursor-pointer transition-colors ease-in-out duration-200 ' \
                       'focus:outline-none disabled:opacity-70 disabled:cursor-not-allowed ' \
                       'disabled:pointer-events-none bg-gray-200 dark:bg-white/10 '
        self.fields['detail'].widget.attrs[
            'class'] = 'filament-forms-textarea-component block w-full rounded-lg border-none px-3 py-2 shadow-sm ' \
                       'ring-1 ring-inset transition duration-75 focus:ring-2 focus:ring-inset focus:ring-primary-500 ' \
                       'disabled:opacity-70 sm:py-2.5 sm:text-sm dark:bg-gray-700 dark:text-white dark:ring-gray-600 ' \
                       'dark:focus:ring-primary-500 ring-gray-300 '
        self.fields['sort_item'].widget.attrs[
            'class'] = 'block w-full rounded-lg border-none px-3 py-2 text-gray-900 shadow-sm ring-1 ring-inset ' \
                       'transition duration-75 focus:ring-2 focus:ring-inset focus:ring-primary-500 ' \
                       'disabled:opacity-70 sm:py-2.5 sm:text-sm dark:bg-gray-700 dark:text-white ' \
                       'dark:focus:ring-primary-500 ring-gray-300 dark:ring-gray-600 '


class TaskCreateForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=True)

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.base_fields["name"].error_messages[
            "required"
        ] = "Please enter Task title."
        self.base_fields["description"].error_messages[
            "required"
        ] = "Please enter Task description."

    class Meta:
        model = Task
        fields = ('name', 'description',)


class MessageForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(), required=True)

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['required'] = True

    class Meta:
        model = Message
        fields = (
            "text",
        )


class AdminTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "name",
            "created_by",
            "project",
            "type",
            "description"
        )

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].widget.attrs['class'] = 'w-full rounded-lg border-gray-300'
        self.fields['type'].widget.attrs['class'] = 'w-full rounded-lg border-gray-300'
        self.fields['created_by'].widget.attrs['class'] = 'w-full rounded-lg border-gray-300'
        self.fields['project'].empty_label = 'Select an option'
        self.fields['type'].empty_label = 'Select an option'
        self.fields['created_by'].empty_label = 'Select an option'
        self.fields["name"].error_messages[
            "required"
        ] = "Please enter Task title."
        self.fields["description"].error_messages[
            "required"
        ] = "Please enter Task description."

    def clean_project(self, *args, **kwargs):
        project = self.cleaned_data["project"]
        if not project:
            raise ValidationError(
                "Please select Project"
            )
        return project

    def clean_created_by(self, *args, **kwargs):
        created_by = self.cleaned_data["created_by"]
        if not created_by:
            raise ValidationError(
                "Please select User"
            )
        return created_by

    def clean_type(self, *args, **kwargs):
        type = self.cleaned_data["type"]
        if not type:
            raise ValidationError(
                "Please select Type"
            )
        return type


class AdminCommentForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = (
            "text",
            "task",
            "user",
        )

    def __init__(self, *args, **kwargs):
        super(AdminCommentForm, self).__init__(*args, **kwargs)
        self.fields['task'].widget.attrs['class'] = 'w-full rounded-lg border-gray-300'
        self.fields['user'].widget.attrs['class'] = 'w-full rounded-lg border-gray-300'
        self.fields['task'].empty_label = 'Select an option'
        self.fields['user'].empty_label = 'Select an option'
        self.fields['text'].required = True
        self.fields["text"].error_messages[
            "required"
        ] = "Please enter description."

    def clean_task(self, *args, **kwargs):
        task = self.cleaned_data["task"]
        if not task:
            raise ValidationError(
                "Please select Item"
            )
        return task

    def clean_user(self, *args, **kwargs):
        user = self.cleaned_data["user"]
        if not user:
            raise ValidationError(
                "Please select user"
            )
        return user


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "email",
            "role",
        )

    def __init__(self, *args, **kwargs):
        super(AdminUserForm, self).__init__(*args, **kwargs)
        self.fields['role'].widget.attrs[
            'class'] = 'block w-full rounded-lg border-none px-3 py-2 text-gray-900 shadow-sm ring-1 ring-inset ' \
                       'transition duration-75 focus:ring-2 focus:ring-inset focus:ring-primary-500 ' \
                       'disabled:opacity-70 sm:py-2.5 sm:text-sm dark:bg-gray-700 dark:text-white ' \
                       'dark:focus:ring-primary-500 ring-gray-300 dark:ring-gray-600 '
        self.fields['first_name'].required = True
        self.fields['role'].required = False
        self.fields['role'].empty_label = 'Select an option'

        self.fields["first_name"].error_messages[
            "required"
        ] = "Please enter name."

        self.fields["email"].error_messages[
            "required"
        ] = "Please enter email."

    def clean(self):

        super(AdminUserForm, self).clean()

        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username and User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            self._errors['username'] = self.error_class([
                'Username already exits'])

        if email and User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            self._errors['email'] = self.error_class([
                'Email already exits'])

        return self.cleaned_data

    def clean_role(self, *args, **kwargs):
        role = self.cleaned_data["role"]
        if not role:
            raise ValidationError(
                "Please select role"
            )
        return role


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = (
            "user",
            "subscribed",
        )

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs[
            'class'] = 'block w-full rounded-lg border-none px-3 py-2 text-gray-900 shadow-sm ring-1 ring-inset ' \
                       'transition duration-75 focus:ring-2 focus:ring-inset focus:ring-primary-500 ' \
                       'disabled:opacity-70 sm:py-2.5 sm:text-sm dark:bg-gray-700 dark:text-white ' \
                       'dark:focus:ring-primary-500 ring-gray-300 dark:ring-gray-600 '
        self.fields['subscribed'].widget.attrs[
            'class'] = 'filament-forms-toggle-component relative inline-flex border-2 border-transparent ' \
                       'shrink-0 ' \
                       'h-6 w-11 rounded-full cursor-pointer transition-colors ease-in-out duration-200 ' \
                       'focus:outline-none disabled:opacity-70 disabled:cursor-not-allowed ' \
                       'disabled:pointer-events-none bg-gray-200 dark:bg-white/10 '
        self.fields['user'].empty_label = 'Select an user'
        self.fields['user'].required = False

    def clean_user(self, *args, **kwargs):
        user = self.cleaned_data["user"]
        if not user:
            raise ValidationError(
                "Please select user"
            )
        return user
