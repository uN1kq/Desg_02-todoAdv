from django.urls import path
from .views import *

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('loginpage/',CustomerLogin.as_view(), name="LoginPage"),
    path('logout/',LogoutView.as_view(next_page='LoginPage'), name="LogOut"),
    path('register/',RegisterPage.as_view(), name="Register"),

    path('', TaskList.as_view(), name='taskList'),
    path('taskDetail/<int:pk>/', TaskDetail.as_view(), name='taskDetail'),
    path('taskCreate/', TaskCreate.as_view(), name='taskCreate'),
    path('taskUpdate/<int:pk>/', TaskUpdate.as_view(), name='taskUpdate'),
    path('taskDelete/<int:pk>/', TaskDelete.as_view(), name='taskDelete'),

]