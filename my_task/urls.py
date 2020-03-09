from django.urls import path
from my_task import views

urlpatterns = [
    path('', views.index),
    path('nav', views.nav),
    path('create_task', views.create_task),
    path('query_tasks', views.query_tasks),
    path('task_info', views.task_info),
    path('accept_task', views.accept_task),
    path('enter_task', views.enter_task),
    path('evaluate_task', views.evaluate_task),
    path('get_my_task', views.get_my_task),
    path('get_my_accept_task', views.get_my_accept_task),
    path('get_task_len', views.get_task_len),
    path('get_evaluate', views.get_evaluate),
    path('collect_task', views.collect_task),
    path('get_collect_tasks', views.get_collect_tasks),
]
