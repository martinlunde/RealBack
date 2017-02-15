from django.shortcuts import render


def login_page(request):
    return render(request, 'templates/lecturer/login_page.html', {})
