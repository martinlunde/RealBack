
from django.shortcuts import render, redirect
from . import forms


def register(request):
    """ Register a new user """
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('lecturer:front_page')

    else:
        form = forms.UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
