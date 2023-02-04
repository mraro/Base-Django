import os

from django.db.models import Q
from django.shortcuts import render, get_list_or_404, get_object_or_404, Http404  # object é para um só elemento
from .models import Remedios

from utility.paginator import make_paginations

RANGE_PER_PAGE = int(
    os.environ.get("PER_PAGE", 6))  # constant (means that not be modified, but you can) its a var global too.


# os.environ.get("PER_PAGE", 6) is a variable of system, that was set in .env and if not found use 6 in this case

# https://docs.djangoproject.com/pt-br/3.2/topics/db/queries/#complex-lookups-with-q-objects
def home(request):
    medicines = Remedios.objects.all().order_by('-id')
    pages = make_paginations(request, medicines, RANGE_PER_PAGE, 9)

    # messages.success(request, "UMA MENSAGEM ENVIADA DO SERVIDOR de SUCCESS")

    # a pasta templantes que herda a pasta home esta linkada na settings do django
    return render(request, "pages/home.html",
                  context={
                      # 'remedios': result[page],
                      'remedios': pages['medicines_page'],
                      'pages': pages,
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
    # messages.error(request, "UMA MENSAGEM ENVIADA DO SERVIDOR de ERROR")

    # medicine = get_list_or_404(Remedios, category__id=idcategoria)  # ISSO É UMA LISTA DO PYTHON
    medicine = get_list_or_404(Remedios.objects.filter(category__id=idcategoria).order_by('-id'))
    pages = make_paginations(request, medicine, RANGE_PER_PAGE)

    return render(request, "pages/category-view.html",
                  context={
                      # 'remedios': medicine,
                      'remedios': pages['medicines_page'],
                      'pages': pages,
                      'categoryTitle': f'{medicine[0].category.name}',  # ISSO É PY: F'{ VARIAVEL}' RETORNA STRING
                      'is_detail': False,
                  })


def search(request):
    var_site = request.GET.get("q")
    if not var_site:
        raise Http404
    else:
        var_site = var_site.strip()  # # '''o | juntamente a função Q faz com que a pesquisa seja OR '''
        medicine = Remedios.objects.filter(Q(title__contains=var_site) | Q(description__contains=var_site)).order_by(
            '-id')
        medicine = medicine.filter(is_published=True)

    pages = make_paginations(request, medicine, RANGE_PER_PAGE)

    return render(request, "pages/search.html", context={
        'remedios': pages['medicines_page'],
        'pages': pages,
        'search_done': var_site, })
