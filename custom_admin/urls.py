from django.urls import path

from custom_admin import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.AdminHomeView.as_view(), name='admin_home'),
    path('projects/', views.ProjectList.as_view(), name='projects'),
    path('items/', views.AdminTaskList.as_view(), name='tasks'),
    path('comments/', views.CommentsList.as_view(), name='comments'),
    path('inbox/', views.InboxList.as_view(), name='inbox'),
    path('add_new_project/', views.ProjectCreateView.as_view(), name='new_project'),
    path('add_new_task/', views.TaskCreateView.as_view(), name='new_task'),
    path('update_project/<slug:slug>', views.ProjectUpdateView.as_view(), name='update_project'),
    path('delete_project/<slug:slug>', views.ProjectDeleteView.as_view(), name='delete_project'),
    path('update_task/<slug:slug>', views.TaskUpdateView.as_view(), name='update_task'),
    path('delete_task/<slug:slug>', views.TaskDeleteView.as_view(), name='delete_task'),
    path('update_comment/<int:pk>', views.CommentUpdateView.as_view(), name='update_comment'),
    path('delete_comment/<int:pk>', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('add_new_comment/', views.CommentCreateView.as_view(), name='new_comment'),
    path('change_task_status/', views.ChangeTaskStatus.as_view(), name='change_task_status'),
    path('users/', views.AdminUserList.as_view(), name='users'),
    path('update_user/<int:pk>', views.UserUpdateView.as_view(), name='update_user'),
    path('new_user/', views.UserCreateView.as_view(), name='new_user'),
    path('delete_user/<int:pk>', views.UserDeleteView.as_view(), name='delete_user'),
    path('votes/', views.AdminVoteList.as_view(), name='votes'),
    path('delete_vote/<int:pk>', views.VoteDeleteView.as_view(), name='delete_vote'),
    path('change_task_vote/', views.ChangeVote.as_view(), name='change_task_vote'),
    path('change_task_subscription_status/', views.ChangeTaskSubscription.as_view(), name='change_task_subscription'),
    path('colors/', views.AdminThemeView.as_view(), name='theme'),
    path('settings/', views.AdminSettingsView.as_view(), name='settings'),
    path('system/', views.AdminSystemView.as_view(), name='system'),
    path('get_project_wise_board/', views.ProjectWiseBoard.as_view(), name='get_project_wise_board'),
    path('notification/', views.NotificationView.as_view(), name='read_notification'),
    path('remove_og_img/', views.RemoveOGImage.as_view(), name='remove_og_image'),
]
