from django import forms

from custom_admin.models import GeneralSetting


class GeneralNotificationForm(forms.ModelForm):
    class Meta:
        model = GeneralSetting
        exclude = ('created', 'modified', 'default_boards', 'theme_color', 'favicon_img',)

    def __init__(self, *args, **kwargs):
        super(GeneralNotificationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'header_script':
                self.fields[field_name].widget.attrs[
                    'class'] = 'filament-forms-toggle-component relative inline-flex border-2 border-transparent ' \
                               'shrink-0 ' \
                               'h-6 w-11 rounded-full cursor-pointer transition-colors ease-in-out duration-200 ' \
                               'focus:outline-none disabled:opacity-70 disabled:cursor-not-allowed ' \
                               'disabled:pointer-events-none bg-gray-200 dark:bg-white/10 '
        self.fields['header_script'].widget.attrs['rows'] = 10
        self.fields['header_script'].widget.attrs['cols'] = 50
        self.fields['password_protect'].widget.attrs[
            'class'] = 'block w-full rounded-lg border-none px-3 py-2 shadow-sm ring-1 ring-inset transition ' \
                       'duration-75 focus:ring-2 focus:ring-inset focus:ring-primary-500 disabled:opacity-70 ' \
                       'sm:py-2.5 sm:text-sm dark:bg-gray-700 dark:text-white dark:focus:ring-primary-500 ' \
                       'ring-gray-300 dark:ring-gray-600 '

        self.fields['inbox_workflow'].widget.attrs[
            'class'] = 'block w-full rounded-lg border-none px-3 py-2 text-gray-900 shadow-sm ring-1 ring-inset ' \
                       'transition duration-75 focus:ring-2 focus:ring-inset focus:ring-primary-500 ' \
                       'disabled:opacity-70 sm:py-2.5 sm:text-sm dark:bg-gray-700 dark:text-white ' \
                       'dark:focus:ring-primary-500 ring-gray-300 dark:ring-gray-600 '
        self.fields['inbox_workflow'].empty_label = 'Select an option'


class ThemeForm(forms.ModelForm):
    class Meta:
        model = GeneralSetting
        fields = ('theme_color', 'favicon_img',)

    def __init__(self, *args, **kwargs):
        super(ThemeForm, self).__init__(*args, **kwargs)
        self.fields['theme_color'].widget.attrs[
            'class'] = 'block w-full rounded-lg border-none px-3 py-2 shadow-sm ring-1 ring-inset transition ' \
                       'duration-75 focus:ring-2 focus:ring-inset focus:ring-primary-500 disabled:opacity-70 ' \
                       'sm:py-2.5 sm:text-sm dark:bg-gray-700 dark:text-white dark:focus:ring-primary-500 ' \
                       'ring-gray-300 dark:ring-gray-600 '
