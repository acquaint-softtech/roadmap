from ckeditor.widgets import CKEditorWidget
from django import forms

from project.models import Project, Task, Message, Board
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
        if Project.objects.filter(title=title, created_by=self.user).exists():
            raise forms.ValidationError("Project already exits.")
        return title


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        exclude = ('created', 'modified',)


class TaskCreateForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=CKEditorWidget(), required=True)

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.fields["name"].error_messages[
            "required"
        ] = "Please enter Task title."
        self.fields["description"].error_messages[
            "required"
        ] = "Please enter Task description."


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
        self.fields["type"].queryset = Board.objects.none()

        if project:
            self.fields["type"].queryset = Board.objects.filter(project_id = int(project))

        self.fields['project'].widget.attrs['class'] = 'form-select appearance-none \
                           block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white \
                           bg-clip-padding bg-no-repeat \
                            border border-solid border-gray-300 rounded transition ease-in-out m-0 \
                            focus:text-gray-700 focus:bg-white \
                            focus:border-blue-600 focus:outline-none'
        self.fields['type'].widget.attrs['class'] = 'form-select appearance-none \
                                   block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white \
                                   bg-clip-padding bg-no-repeat \
                                    border border-solid border-gray-300 rounded transition ease-in-out m-0 \
                                    focus:text-gray-700 focus:bg-white \
                                    focus:border-blue-600 focus:outline-none'
        self.fields['created_by'].widget.attrs['class'] = 'form-select appearance-none \
                                   block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white \
                                   bg-clip-padding bg-no-repeat \
                                    border border-solid border-gray-300 rounded transition ease-in-out m-0 \
                                    focus:text-gray-700 focus:bg-white \
                                    focus:border-blue-600 focus:outline-none'
        self.fields['project'].required = True
        self.fields['created_by'].required = True
        self.fields['type'].required = True

        self.fields["name"].error_messages[
            "required"
        ] = "Please enter Task title."
        self.fields["description"].error_messages[
            "required"
        ] = "Please enter Task description."


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
        self.fields['task'].widget.attrs['class'] = 'form-select appearance-none \
                           block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white \
                           bg-clip-padding bg-no-repeat \
                            border border-solid border-gray-300 rounded transition ease-in-out m-0 \
                            focus:text-gray-700 focus:bg-white \
                            focus:border-blue-600 focus:outline-none'
        self.fields['user'].widget.attrs['class'] = 'form-select appearance-none \
                                   block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white \
                                   bg-clip-padding bg-no-repeat \
                                    border border-solid border-gray-300 rounded transition ease-in-out m-0 \
                                    focus:text-gray-700 focus:bg-white \
                                    focus:border-blue-600 focus:outline-none'

        self.fields['task'].required = True
        self.fields['user'].required = True
        self.fields["text"].error_messages[
            "required"
        ] = "Please enter description."


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
        )

    def __init__(self, *args, **kwargs):
        super(AdminUserForm, self).__init__(*args, **kwargs)
        self.fields['role'].widget.attrs['class'] = 'form-select appearance-none \
                           block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white \
                           bg-clip-padding bg-no-repeat \
                            border border-solid border-gray-300 rounded transition ease-in-out m-0 \
                            focus:text-gray-700 focus:bg-white \
                            focus:border-blue-600 focus:outline-none'

        self.fields['role'].required = True
        self.fields["username"].error_messages[
            "required"
        ] = "Please enter username."
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
