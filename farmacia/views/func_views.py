import os

from django.db.models import Q, Count, F, Value
from django.db.models.functions import Concat
from django.shortcuts import render, get_list_or_404, get_object_or_404, Http404  # object é para um só elemento

from farmacia.models import Remedios, Category

from utility.paginator import make_pagination

# constant (means that not be modified, but you can in .env file) its a var global too.
RANGE_PER_PAGE = int(os.environ.get("RANGE_PER_PAGE", 6))
OBJ_PER_PAGE = int(os.environ.get("OBJ_PER_PAGE", 9))


# https://docs.djangoproject.com/pt-br/3.2/topics/db/queries/#complex-lookups-with-q-objects
# https://docs.djangoproject.com/pt-br/4.0/ref/models/querysets/#field-lookups
# https://docs.djangoproject.com/pt-br/4.0/ref/models/querysets/#operators-that-return-new-querysets
def home(request):
    medicines = Remedios.objects.get_published()
    category = Category.objects.filter(remedios__isnull=False, remedios__is_published=True).distinct()  # DISTINCT
    # REMOVES DUPLICATES

    medicines = medicines.annotate(  # GIVE MORE ONE VARIABLE INTO A LIST OF QUERYSET
                author_full_name=Concat(
                    F('author__first_name'),
                    Value(" "),
                    F('author__last_name'),
                )
            )
    medicines = medicines.select_related('author', 'category')  # ! THIS IMPROVE DATABASE READ

    # medicines = medicines.select_related('author', 'category')  # THIS IMPROVES READ DATABASE (WORKS ON FOREIGN KEY)
    pages = make_pagination(request, medicines, RANGE_PER_PAGE, OBJ_PER_PAGE)
    # a pasta templates que herda a pasta home esta linkada na settings do django
    return render(request, "pages/home.html",
                  context={
                      # 'remedios': result[page],
                      'remedios': pages['medicines_page'],
                      'pages': pages,
                      "nameSite": "Farma func",
                      'categories': category,

                      # 'remedios': [factory.make_recipe() for _ in range(10)]  # CRIA UM DICIONARIO DENTRO DO
                      # DICIONARIO

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
    medicine = get_list_or_404(
        Remedios.objects.filter(category__id=idcategoria).order_by('-id').select_related('author', 'category')
    )

    pages = make_pagination(request, medicine, RANGE_PER_PAGE)

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
        medicine = Remedios.objects.filter(Q(title__contains=var_site) |
                                           Q(description__contains=var_site) |
                                           Q(category__contains=var_site)).order_by('-id')
        medicine = medicine.filter(is_published=True)
        medicine = medicine.select_related('author', 'category')

    pages = make_pagination(request, medicine, RANGE_PER_PAGE)

    return render(request, "pages/search.html", context={
        'remedios': pages['medicines_page'],
        'pages': pages,
        'search_done': var_site, })


def theory(request):
    remedio = Remedios.objects.all()
    remedio = remedio.values('title', 'price', 'author', 'created_at', 'category')[:10]  # desempacotamento
    num_of_objects = remedio.aggregate(Count('id'))
    context = {
        'remedio': remedio,
        'num_len': num_of_objects,
    }
    return render(request, 'pages/theory.html', context=context)
