## import needed libraries/models
from pickletools import read_unicodestring8
from turtle import title
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    FormView,
)

from django.contrib.auth.views import(LoginView)
from django.contrib.auth.mixins import(LoginRequiredMixin)
from django.contrib.auth.forms import(UserCreationForm)
from django.contrib.auth import(login)


from .models import ToDoList, ToDoItem

##create views which django uses to know what to do with data given
##LoginRequiredMixin is included so that users only have access to their own to-do lists
##model uses models created in models.py, and all other views purely use django templates, however all views herein use a django view as a framework

class CustomLoginView(LoginView):
    template_name = 'todo_app/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

class RegisterPage(FormView):
    template_name = 'todo_app/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterPage, self).get(*args, **kwargs)

class ListListView(LoginRequiredMixin, ListView):
    model = ToDoList
    template_name = 'todo_app/index.html'
    context_object_name = "list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = context['list'].filter(user=self.request.user)
        
        search_input = self.request.GET.get('search-lists') or ''
        if search_input:
            context['list'] = context['list'].filter(title__icontains = search_input)
        
        return context

class ItemListView(LoginRequiredMixin, ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"
    context_object_name = "items"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id = self.kwargs["list_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = ToDoList.objects.get(id = self.kwargs["list_id"])
        context['items'] = context['items'].filter(user=self.request.user)
        context['count'] = context['items'].filter(complete = False).count()

        search_input = self.request.GET.get('search-item') or ''

        if search_input:
            context['items'] = context['items'].filter(title__icontains = search_input)

        return context

class ListCreate(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields  = ["title"]

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(ListCreate, self).form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context

class ItemCreate(LoginRequiredMixin, CreateView):
    model = ToDoItem
    fields = ['todo_list','title', 'description','due_date','complete']

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self,**kwargs):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(ItemCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

    context_object_name = "items"

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoItem
    fields = ['todo_list','title', 'description','due_date','complete']

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

    context_object_name = "items"

class ListDelete(LoginRequiredMixin, DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context