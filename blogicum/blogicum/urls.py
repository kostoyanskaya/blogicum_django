from django.contrib import admin
from django.views.generic.edit import CreateView
from django.urls import include, path, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from . import views
from django.shortcuts import render, redirect


handler404 = 'pages.views.page_not_found'
handler403 = 'pages.views.csrf_failure'

handler500 = 'pages.views.tr_handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', views.register_user, name='registration'),
]
