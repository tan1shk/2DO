from django.shortcuts import redirect 

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


class TaskLogin(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('list_view')

class TaskSignup(FormView):
    template_name = 'base/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('list_view')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(TaskSignup, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('list_view')
        return super(TaskSignup, self).get(*args, **kwargs)
    

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context

 
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    login_url = 'login'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'base/task_create.html'
    fields = ['title', 'decription']
    success_url = reverse_lazy('list_view')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    template_name = 'base/task_update.html'
    fields = ['title', 'decription', 'complete']
    success_url = reverse_lazy('list_view')
    login_url = 'login'


def delete(request, pk):   
        Task.objects.filter(id=pk).delete()
        return redirect('list_view')


def uupdate_complete(request, pk):
    Task.objects.filter(id=pk).update(complete=True)
    return redirect('list_view')


def uupdate_incomplete(request, pk):
    Task.objects.filter(id=pk).update(complete=False)
    return redirect('list_view')