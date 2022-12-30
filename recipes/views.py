from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, "pages/home.html", context={
        "nome":"Alessandro Oliveira",
    })

def contato(request):
    return HttpResponse("CONTATO")

def sobre(request):
    return HttpResponse("SOBRE")