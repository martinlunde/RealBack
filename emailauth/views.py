
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """ Register a new user """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # TODO save user
            return HttpResponseRedirect('lecturer:front_page')

    else:
        form = UserCreationForm()

    # render(request, 'templates/registration/register.html', {'form': form})
    pass
