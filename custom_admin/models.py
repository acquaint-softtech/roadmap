from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from colorfield.fields import ColorField
from common.models import TimeStampModel


# Create your models here.

class GeneralSettings(TimeStampModel):
    center_board_project_view = models.BooleanField(default=True,
                                                    help_text='When centering, this will always show the boards in '
                                                              'the center of the content area.')
    center_default_board = models.BooleanField(default=True,
                                               help_text='When creating a new project, some default boards can be '
                                                         'created.')
    project_in_sidebar = models.BooleanField(default=True,
                                             help_text="If you don't want to show projects without boards in the "
                                                       "sidebar, toggle this off.")
    allow_general_creation = models.BooleanField(default=True,
                                                 help_text='This allows your users to create an item without a board.')
    enable_item_age = models.BooleanField(default=False,
                                          help_text='Enable this to show the age of an item on the details page.')
    enable_voter_avtar = models.BooleanField(default=True,
                                             help_text='Enabling this will show the avatars of the most recent voters '
                                                       'when viewing an item.')
    user_select_project = models.BooleanField(default=True)
    is_project_required = models.BooleanField(default=False)
    is_select_board = models.BooleanField(default=True)
    is_board_required = models.BooleanField(default=False)
    is_user_verify_email = models.BooleanField(default=True)
    welcome_text = RichTextField(null=True, default='Welcome to our roadmap!')
    password_protect = models.CharField(max_length=100, blank=True, null=True)
    enable_change_log = models.BooleanField(default=False)
    block_robost = models.BooleanField(default=False, help_text="Instructs your roadmap to add the block robots META "
                                                                "tag, it's up to the search engines to honor this "
                                                                "request.")

    header_script = models.TextField(null=True, blank=True)
    default_boards = ArrayField(
        models.CharField(max_length=512), default=['Under Review', 'Planned', 'In progress', 'Live', 'Closed']
    )
    theme_color = ColorField(default='#d42020')
    favicon_img = models.ImageField(null=True,blank=True)


    workflow_choice = (
        ("item_disabled", "Disabled"),
        ("without-board-and-project", "Items without board and project"),
        ("without-board-or-project", "Items without board or project"),
        ("without-board", "Items without board"),
    )

    inbox_workflow = models.CharField(max_length=60,
                                      choices=workflow_choice,
                                      null=True, blank=True)
