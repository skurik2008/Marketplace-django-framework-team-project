from django.shortcuts import render
from django.views import View


def TestView(request):
    return render(request, 'test.html')
