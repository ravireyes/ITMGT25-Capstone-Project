# todo_list/todo_app/urls.py
## import the views and path to create a URL dispatcher
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

## each url is given a path, a view to use and a name to use when referencing the url
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name = 'login'),

    path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout'),

    path('register/', views.RegisterPage.as_view(), name = 'register'),

    path('', views.ListListView.as_view(), name = 'index'),

    path('lists/<int:list_id>/', views.ItemListView.as_view(), name = 'list'),

    path('lists/add/', views.ListCreate.as_view(), name='list-add'),

    path("lists/<int:pk>/delete/", views.ListDelete.as_view(), name = "list-delete"),
    
    path(
        "lists/<int:list_id>/item/add/",
        views.ItemCreate.as_view(),
        name = 'item-add',
    ),
    path(
        "lists/<int:list_id>/item/<int:pk>/",
        views.ItemUpdate.as_view(),
        name = 'item-update',
    ),
    path(
        "lists/<int:list_id>/item/<int:pk>/delete/",
        views.ItemDelete.as_view(),
        name = "item-delete",
    ),
    path(
        "", views.ListListView.as_view(), name = 'return'
    ),
]