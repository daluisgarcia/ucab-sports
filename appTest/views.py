from django.shortcuts import render, redirect

def index(request):
    return render(request, 'appTest/index.html', context=None)