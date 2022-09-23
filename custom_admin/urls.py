from django.urls import path

from custom_admin import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.AdminHomeView.as_view(), name='admin_home'),
    path('projects/', views.ProjectList.as_view(), name='projects'),
    path('tasks/', views.AdminTaskList.as_view(), name='tasks'),
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
]
