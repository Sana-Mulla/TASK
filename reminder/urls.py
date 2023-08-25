from django.urls import path
from reminder import views

app_name = 'reminder'
urlpatterns = [
    # urls for template
    path('base/',views.base),
    path('', views.ReminderList.as_view(), name='tasks'),
    path('task/add/', views.ReminderCreate.as_view(), name='task_add'),
    path('task-update/<int:pk>/',
         views.ReminderUpdate.as_view(), name='task_update'),
    path('task/<int:pk>/delete/',
         views.ReminderDelete.as_view(), name='task_delete'),
    path('task/<int:pk>/finish/',
         views.finish_task, name='finish_task'),
    # urls for API
    path('create-task/', views.CreateTask, name ='create-task'),
    path('task-list/', views.taskList, name="task-list"),
    path('task-detail/<int:pk>/', views.taskDetail, name="task-detail"),
    path('task-update/<str:pk>/', views.taskUpdate, name="task-update"),
    path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
    
]
