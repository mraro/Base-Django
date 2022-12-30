from django.shortcuts import render
from django.http import HttpResponse
from farmacia.utils.remediosautofill import factory

def home(request):
    # a pasta templantes que herda a pasta home esta linkada na settings do django
    return render(request, "pages/home.html",
                  context={
                      'remedios':[factory.make_recipe() for _ in range(10)]  # CRIA UM DICIONARIO DENTRO DO DICIONARIO

                  # context={
                  #     "nomefarmacia":"Nome da Farmacia",
                  #     "qtdePorPagina":"10",
                  #     "nomeUsuario":"none",
    })

def remedios(request, idremedios):
    return render(request,"pages/remedio-view.html",
                  context={
                      'remedio':factory.make_recipe(),  #CRIA UM SIMPLES DICIONARIO
                      'is_detail':True,
    })


def cadastro(request):
    return HttpResponse("CADASTRO")