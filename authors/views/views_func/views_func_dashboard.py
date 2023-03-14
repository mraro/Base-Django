from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _

from authors.forms import EditObjectForm
from farmacia import models


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    remedios = models.Remedios.objects.filter(is_published=False, author=request.user)
    # print(request.user.first_name)
    return render(request, 'pages/dashboard.html', context={
        'remedios': remedios,

    })


@login_required(login_url='authors:login', redirect_field_name='next')
def edit_obj(request, idobject):
    remedio = models.Remedios.objects.filter(id=idobject, is_published=False, author=request.user)
    form = EditObjectForm(
        data=request.POST or None,  # receive a request data or none
        files=request.FILES or None,
        instance=remedio[0]  # if none receive what will be edited
    )
    if form.is_valid():
        object_data = form.save(commit=False)
        # print(type(object_data.author))

        object_data.is_published = False
        object_data.save()

        messages.success(request, _("Medicine Saved"))
        return redirect(reverse('authors:dashboard'))

    return render(request, 'pages/edit_obj_view.html', context={
        # 'remedio': remedio[0],
        'form': form,
        'form_button': _('Save'),
        'edit':'tru',
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def create_obj(request):
    author = models.User.objects.get(username=request.user)
    form = EditObjectForm(
        data=request.POST or None,
        files=request.FILES or None,
    )
    # print(author)
    if form.is_valid():
        object_data = form.save(commit=False)
        object_data.is_published = False
        object_data.author = author
        object_data.save()
        messages.success(request, _("Medicine Created and send to analise"))
        return redirect(reverse('authors:dashboard'))
    return render(request, 'pages/new_obj_view.html', context={
        'form': form,
        'form_button': _('Save'),
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def delete_obj(request, idobject):
    if not request.POST:
        raise Http404
    remedio = models.Remedios.objects.get(id=idobject, is_published=False, author=request.user)
    titulo = remedio.title

    translated_success = _('deleted')
    translated_fail = _("wasn't deleted")

    if remedio.delete():
        messages.success(request, f"{titulo} {translated_success}!")
    else:
        messages.error(request, f"{titulo} {translated_fail}!")

    return redirect(reverse('authors:dashboard'))
