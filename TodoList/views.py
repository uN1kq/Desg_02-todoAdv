from TodoList.models import task
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.urls import reverse_lazy
from .models import task

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login


# Create your views here.

class CustomerLogin(LoginView):
    template_name = 'TodoList/loginpage.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('taskList')


class RegisterPage(FormView):
    template_name = 'TodoList/registerpage.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('taskList')

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request.user)
        return super(RegisterPage, self).form.is_valid(form) 

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin ,ListView):
    model = task
    context_object_name = 'tasks'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('Seach-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title_startswith=search_input)
        context['search_input'] = search_input 
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = task
    context_object_name = 'mytasks'
    template_name = 'TodoList/mytasks.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = task
    fields = ['title','description','complete']
    success_url = reverse_lazy('taskList')

    def form_valid(self, form):
        form.instance.self= self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = task
    fields = ['title','description','complete']
    success_url = reverse_lazy('taskList')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = task
    context_object_name = 'mytasks'
    success_url = reverse_lazy('taskList')
