from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', RedirectView.as_view(url='list')),

    path('list', views.TaskListView.as_view(), name='taskList'),

    path('create/', views.TaskCreateView.as_view(), name='taskCreate'),

    path('<int:pk>/', views.TaskDetailView.as_view(), name='taskDetail'),

    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='taskUpdate'),

    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='taskDelete'),

    path('<int:pk>/report/create', views.TaskReportCreatView.as_view(), name='taskReportCreate')
]
