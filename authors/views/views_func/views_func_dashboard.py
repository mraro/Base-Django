from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from authors.forms import EditObjectForm
from farmacia import models


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    remedios = models.Remedios.objects.filter(is_published=False, author=request.user)
    # print(request.user.first_name)
    return render(request, 'pages/dashboard.html', context={
        'remedios': remedios,

    })


# @login_required(login_url='authors:login', redirect_field_name='next')
# def edit_obj(request, idobject):
#     remedio = models.Remedios.objects.filter(id=idobject, is_published=False, author=request.user)
#     form = EditObjectForm(
#         data=request.POST or None,  # receive a request data or none
#         files=request.FILES or None,
#         instance=remedio[0]  # if none receive what will be edited
#     )
#     if form.is_valid():
#         object_data = form.save(commit=False)
#         # print(type(object_data.author))
#
#         object_data.is_published = False
#         object_data.save()
#
#         messages.success(request, "Remedio Salvo")
#         return redirect(reverse('authors:dashboard'))
#
#     return render(request, 'pages/edit_obj_view.html', context={
#         # 'remedio': remedio[0],
#         'form': form,
#         'form_button': 'Salvar',
#         'edit':'tru',
#     })


# @login_required(login_url='authors:login', redirect_field_name='next')
# def create_obj(request):
#     author = models.User.objects.get(username=request.user)
#     form = EditObjectForm(
#         data=request.POST or None,
#         files=request.FILES or None,
#     )
#     # print(author)
#     if form.is_valid():
#         object_data = form.save(commit=False)
#         object_data.is_published = False
#         object_data.author = author
#         object_data.save()
#         messages.success(request, "Remedio criado e enviado a analise")
#         return redirect(reverse('authors:dashboard'))
#     return render(request, 'pages/new_obj_view.html', context={
#         'form': form,
#         'form_button': 'Salvar',
#     })


# @login_required(login_url='authors:login', redirect_field_name='next')
# def delete_obj(request, idobject):
#     if not request.POST:
#         raise Http404
#     remedio = models.Remedios.objects.get(id=idobject, is_published=False, author=request.user)
#     titulo = remedio.title
#
#     if remedio.delete():
#         messages.success(request, f"{titulo} deletado!")
#     else:
#         messages.error(request, f"{titulo} não foi deletado!")
#
#     return redirect(reverse('authors:dashboard'))
