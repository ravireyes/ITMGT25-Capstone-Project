from django.contrib import admin
from todo_app.models import ToDoItem, ToDoList

## app models are registered so that they can be used with admin function of django

# Register your models here.
admin.site.register(ToDoItem)
admin.site.register(ToDoList)