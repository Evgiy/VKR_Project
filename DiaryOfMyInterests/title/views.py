from django.shortcuts import render
from django.http import HttpResponse

def title(request):
    return render(request, 'title/title.html')


