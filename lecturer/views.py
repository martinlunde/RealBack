
from django.shortcuts import render


def lecturer(request):
    # if already logged in:


    # else serve login page
    return render(request, 'templates/lecturer/login_page.html', {})

