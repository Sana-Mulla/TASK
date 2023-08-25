from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.db.models import F
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reminder.models import Task
from reminder.forms import ReminderCreateForm, ReminderUpdateForm

from reminder.serializers import TaskSerializer

User = get_user_model()


# Views for template
def base(request):
    return render(request,'reminder/base.html')

class ReminderList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'all_tasks'
    template_name = 'reminder/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by(F('due_date').asc(nulls_last=True))


class ReminderCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = ReminderCreateForm
    template_name = 'reminder/task_add.html'
    success_url = reverse_lazy('reminder:tasks')

    def form_valid(self, form):
        # the authenticated user will be set as the owner of the task
        form.instance.owner = self.request.user
        return super().form_valid(form)





class ReminderUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = ReminderUpdateForm
    template_name = 'reminder/task_update.html'
    success_url = reverse_lazy('reminder:tasks')


class ReminderDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('reminder:tasks')


def finish_task(request, pk):
    task = Task.objects.get(id=pk)
    task.is_finished = True
    task.save()

    return redirect('reminder:tasks')


# views for API

@api_view(['GET'])
def taskList(request):
	tasks = Task.objects.all()
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)


@api_view(['POST'])
def CreateTask(request):
	serializer = TaskSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()
		print(serializer.data)

	return Response(serializer.data)


@api_view(['GET'])
def taskDetail(request, pk):
	tasks = Task.objects.get(id=pk)
	serializer = TaskSerializer(tasks, many=False)
	return Response(serializer.data)


@api_view(['PUT'])
def taskUpdate(request, pk):
	task = Task.objects.get(id=pk)
	serializer = TaskSerializer(instance=task, data=request.data,partial=False)
   
	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
	task = Task.objects.get(id=pk)
	task.delete()

	return Response('Item succsesfully delete!')


