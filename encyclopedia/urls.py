from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry_page, name="entry_page"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>", views.edit_page, name='edit_page'),
    path("random/", views.random_page ,name='random_page'),
    #when the URL ends with '/random/', Django should route the request to the 'random_page' view function
    #view.random_page is the view function in the views.py that will handle the HTTP request 
    # name="random_page" is a unique name given to this URL pattern. It allows you to refer to this specific URL pattern by its name in Django's URL related functions 
    #<str:title> is a path converter that captures any string value and assigns it to the variable 'title'
]
