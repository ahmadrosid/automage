from django.urls import path

from . import views

urlpatterns = [
    path('', view=views.home, name='landing'),
    path('jobs', view=views.cronjob_list, name='cronjob_list'),
    path('jobs/<int:pk>', view=views.cronjob_delete, name='cronjob_delete'),
    path('jobs/edit/<int:pk>', view=views.cronjob_edit, name='cronjob_edit'),
    path('jobs/create', view=views.cronjob_create, name='cronjob_create'),
    path('home', view=views.home, name='home')
]
