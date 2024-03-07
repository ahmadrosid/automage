from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', view=views.register, name='register'),
    path('', include('jobs.urls')),
    path('', include('django.contrib.auth.urls')),
]
