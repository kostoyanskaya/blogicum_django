from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.isvalid():
            form.save()
            return redirect(reverse_lazy('blog:index'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {'form': form})
