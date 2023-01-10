from django.shortcuts import render, get_list_or_404, get_object_or_404, Http404  # object é para um só elemento
from django.http import HttpResponse
from farmacia.utils.remediosautofill import factory
from .models import Remedios


def home(request):
    medicine = Remedios.objects.all().order_by('-id')

    # a pasta templantes que herda a pasta home esta linkada na settings do django
    return render(request, "pages/home.html",
                  context={
                      'remedios': medicine,
                      # "nomefarmacia": "Farma TOP",

                      # 'remedios': [factory.make_recipe() for _ in range(10)]  # CRIA UM DICIONARIO DENTRO DO
                      # DICIONARIO

                      #      context={
                      #     "qtdePorPagina":"10",
                      #     "nomeUsuario":"none",
                  })


def remedios(request, idremedios):
    # medicine = Remedios.objects.get(id=idremedios)
    medicine = get_object_or_404(Remedios, id=idremedios)
    return render(request, "pages/remedio-view.html",

                  context={
                      'remedio': medicine,
                      # 'remedio': factory.make_recipe(),  # CRIA UM SIMPLES DICIONARIO
                      'is_detail': True,
                  })


def categoria(request, idcategoria):
    # medicine = Remedios.objects.filter(category__id=idcategoria).order_by('-id') # ISSO É BASICO

    # medicine = get_list_or_404(Remedios, category__id=idcategoria)  # ISSO É UMA LISTA DO PYTHON

    medicine = get_list_or_404(Remedios.objects.filter(category__id=idcategoria).order_by('-id'))

    return render(request, "pages/category-view.html",
                  context={
                      'remedios': medicine,
                      'categoryTitle': f'{medicine[0].category.name}',  # ISSO É PY: F'{ VARIAVEL}' RETORNA STRING
                      'is_detail': False,
                  })


def search(request):
    var_site = request.GET.get("q")
    if not var_site:
        raise Http404
    else:
        var_site = var_site.strip()
        medicine = Remedios.objects.filter(title__contains=var_site)
    return render(request, "pages/search.html", context={
        'remedios': medicine,
        'search_done': var_site, })


def cadastro(request):
    return HttpResponse("CADASTRO")
