## django models and other functions are imported

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

## define functions and classes to be used in views.py
## proper migrations are needed for models to be available in app

def default_due_date():
    return timezone.now() + timezone.timedelta(days=7)

class ToDoList(models.Model):
    title = models.CharField(max_length = 200, unique = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title

class ToDoItem(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    title = models.CharField(max_length = 250)
    description = models.TextField(null=True, blank = True)
    complete = models.BooleanField(default = False)
    created_date = models.DateTimeField(auto_now_add = True)
    due_date = models.DateTimeField(default=default_due_date)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse(
            'item-update', args=[str(self.todo_list.id), str(self.id)]
        )
        
    def __str__(self):
        return f'{self.title}: due {self.due_date}'

    class Meta:
        ordering = ["complete"]

