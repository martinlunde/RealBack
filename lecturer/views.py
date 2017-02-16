
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def front_page(request):
    # if already logged in
    pass


def login(request):
    """ Users are redirected here if login is required """
    return render(request, 'templates/lecturer/login_page.html', {})
