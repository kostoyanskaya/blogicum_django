from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import include, path, reverse_lazy
from django.contrib.auth.forms import UserCreationForm

def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def tr_handler500(request):
    return render(request, 'pages/500.html', status=500)


