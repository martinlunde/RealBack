
from django.shortcuts import render


def front_page(request):
    # if already logged in:
    pass
    # else serve login page
    return render(request, 'templates/lecturer/login_page.html', {})

