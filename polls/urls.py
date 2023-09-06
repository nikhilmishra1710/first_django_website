from django.urls import path
from django.http import HttpRequest
from . import views

app_name="polls"
urlpatterns=[
    path("", views.IndexView.as_view() , name="index"),
    path("addpoll/", views.addPoll ,name="AddPoll"),
    path("addpoll/add", views.add ,name="add"),
    path("<int:pk>/", views.DetailView.as_view() , name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view() , name="results"),
    path("<int:question_id>/vote/", views.vote , name="vote"),
    path("polls/login", views.LoginPage, name="Login"),
    path("Authuser/", views.Checkuser, name="authuser"),
    path("newuser/", views.newuser, name="newuser"),
    path("polls/logout/",views.logoutfunc,name="logout")
]