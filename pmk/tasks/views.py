from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect,get_object_or_404
from django.contrib import messages
from .models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    template_name = 'tasks/taskList.html'
    context_object_name = 'tasks'
    model = Task


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'tasks/taskDetail.html'
    model = Task



class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'tasks/taskCreate.html'
    success_url = reverse_lazy('tasks:taskList')
    model = Task
    fields = [
        'title',
        'progress',
        'due_date'
    ]
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    template_name = 'tasks/taskUpdate.html'
    fields = [
        'title',
        'progress',
        'due_date'
    ]
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author.id != request.user.id:
            return redirect('tasks:taskList')
        else:
            return super().get(request, *args, **kwargs)


    def form_valid(self, form):
        print(self.object.author.id)
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
