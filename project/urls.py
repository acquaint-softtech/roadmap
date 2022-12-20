from django.urls import path
from project import views

app_name = 'project'

urlpatterns = [
    path('projects/', views.ProjectList.as_view(), name='projects'),
    path('project/<slug:slug>', views.TaskList.as_view(), name='project_detail'),
    path('task/<slug:slug>', views.TaskDetailView.as_view(), name='task_detail'),
    path('save_task/', views.SaveTaskView.as_view(), name='save_task'),
    path('save_comment/', views.SaveCommentView.as_view(), name='save_comment'),
]
