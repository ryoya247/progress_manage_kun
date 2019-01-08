from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect,get_object_or_404
from django.contrib import messages
from .models import Task, Report
import requests, json
import pmk.settings as settings


class TaskListView(LoginRequiredMixin, generic.ListView):
    template_name = 'tasks/taskList.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        myTasks = Task.objects.filter(author = self.request.user.id)
        myCompTasks = Task.objects.filter(author = self.request.user.id).filter(is_complete=True)
        context['myTasks'] = myTasks
        context['myCompTasks'] = myCompTasks
        category_list = {
            'created_at': '作成日',
            'due_date': '期限',
            'title': 'タスク名',
            'progress': '進捗'
        }

        q_category = self.request.GET.get("category")
        q_type = self.request.GET.get("sort_type")

        if q_category != None and q_type != None:
            if q_type == "asc":
                context['myTasks'] = Task.objects.filter(author = self.request.user.id).order_by(q_category)
                messages.success(
                    self.request,
                    '{}，昇順で並び替えました'.format(category_list[q_category]),
                )
                return context
            elif q_type == "desc":
                context['myTasks'] = Task.objects.filter(author = self.request.user.id).order_by(q_category).reverse()
                messages.success(
                    self.request,
                    '{}，降順で並べ替えました'.format(category_list[q_category]),
                )
                return context
            else:
                return context
        else:
            return context



class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'tasks/taskDetail.html'
    model = Task
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        task_pk = self.kwargs.get(self.pk_url_kwarg)
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        taskReports = Report.objects.filter(task = task_pk).order_by('created_at').reverse()
        context['TaskReports'] = taskReports
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'tasks/taskCreate.html'
    success_url = reverse_lazy('tasks:taskList')
    model = Task
    fields = [
        'title',
        'due_date'
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        task = form.save(commit=False)
        task.save()
        messages.success(
            self.request,
            '「{}」を作成しました'.format(task),
        )
        requests.post(settings.SLACK_ENDPOINT,
            data = json.dumps({
                'text': '{}さんがタスクを作成しました'.format(self.request.user),
                "attachments": [
                    {
                        "color": "#36a64f",
                        "fields": [
                            {
                                "title": "{}".format(task.title),
                                "value": "進捗：{}%\n期限：{}".format(task.progress, task.due_date),
                                "short": False
                            }
                        ]
                    }

                ]
            }))
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    template_name = 'tasks/taskUpdate.html'
    fields = [
        'title',
        'due_date'
    ]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author.id != request.user.id:
            return redirect('tasks:taskList')
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        task = form.save(commit=False)
        task.updated_at = timezone.now()
        task.save()
        messages.success(
            self.request,
            '「{}」を更新しました'.format(self.object),
        )
        return redirect('tasks:taskDetail', pk=task.pk)



class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:taskList')
    template_name = 'tasks/taskDelete.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author.id != request.user.id:
            return redirect('tasks:taskList')
        else:
            return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result


class TaskReportCreatView(LoginRequiredMixin, generic.CreateView):
    model = Report
    success_url = reverse_lazy('tasks:taskDetail')
    template_name = 'tasks/taskReportCreate.html'
    fields = [
        'add_progress',
        'text'
    ]

    def get_context_data(self, **kwargs):
        task_pk = self.kwargs.get('pk')
        context = super(TaskReportCreatView, self).get_context_data(**kwargs)
        parent_task = Task.objects.filter(pk = task_pk)
        context['parentTask'] = parent_task
        return context


    def form_valid(self, form):
        task_pk = self.kwargs.get('pk')
        parent_task = get_object_or_404(Task, pk=task_pk)
        form.instance.task = parent_task
        report = form.save(commit=False)

        if report.add_progress + parent_task.progress > 100:
            messages.error(self.request, '進捗の合計は100%以下にしてください')
            return redirect('tasks:taskReportCreate', pk=task_pk)

        report.updated_at = timezone.now()
        report.save()
        parent_task.progress += report.add_progress

        if parent_task.progress == 100:
            parent_task.is_complete = True

        parent_task.save()

        messages.success(self.request, '進捗を更新しました')
        requests.post(settings.SLACK_ENDPOINT,
            data = json.dumps({
                'text': '{}さんが進捗を更新しました'.format(self.request.user),
                "attachments": [
                    {
                        "color": "#36a64f",
                        "fields": [
                            {
                                "title": "{}".format(parent_task.title),
                                "value": "進捗：{}％（ +{}％ ）\n{}".format(parent_task.progress, report.add_progress, report.text),
                                "short": False
                            }
                        ]
                    }

                ]
            }))
        return redirect('tasks:taskDetail', pk=task_pk)
