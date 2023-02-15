from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify

from authors.forms import RegisterForm, LoginForm, EditObjectForm
from farmacia import models


# Create your views here.
def register_view(request):  # request is raw information that comes from browser
    session_data = request.session.get('register_form_data',
                                       None)  # Default None # session is a data that keeps after reload the page
    form = RegisterForm(session_data)  # this is a form created at forms folder( I put some examples there but has
    # more in documentation django)

    return render(request, 'pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:create'),
        'form_button': 'Cadastrar',
    })


def register_create(request):
    if not request.POST:  # Avoid "pilantras" to send get data and crash site
        raise Http404()

    POST = request.POST  # Receive data by POST
    request.session['register_form_data'] = POST  # Give data from POST to SESSION
    form = RegisterForm(POST)

    if form.is_valid:  # form valid is important to able form.save
        try:
            user = form.save(commit=False)  # receive data from form, after valid but don't save yet
            user.set_password(user.password)  # cryptography password
            user.save()  # save data in DB
            messages.success(request, "Usuario Cadastrado com Sucesso!!!")

            del (request.session['register_form_data'])  # kill session
            return redirect('farmacia:home')
        except ValueError:
            messages.error(request, "Falha ao criar o usuario")
            return redirect('authors:register')

    # return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'pages/login_view.html', context={
        'form': form,
        'form_action': reverse('authors:authenticate'),
        'form_button': 'Login',
    })


def login_authenticate(request):
    if not request.POST:
        raise Http404
    POST = request.POST  # Recive data by POST
    # print("\n ", POST, "\n")
    form = LoginForm(POST)

    login_page = reverse('authors:login')

    if form.is_valid:
        # print(form.is_valid)
        user_authenticate = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'),
        )
        # print("\n", user_authenticate, "\n")

        if user_authenticate is not None:
            login(request, user_authenticate)
            messages.success(request, "Sucesso no Login!")
            return redirect(reverse('farmacia:home'))

        else:
            messages.error(request, 'Usuario e/ou senha incorretos')
            return redirect(login_page)

    messages.error(request, 'preencha os campos corretamente')

    return redirect(login_page)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_backend(request):
    if not request.POST:
        raise Http404
    # print(request.POST.get('username'), ' >< ', request.user.username)
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    if request.POST.get('first_name'):
        messages.success(request, f"Até mais {request.POST.get('first_name')}")
    else:
        messages.success(request, f"Até mais {request.POST.get('username')}")

    return redirect(reverse('farmacia:home'))


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

        messages.success(request, "Remedio Salvo")
        return redirect(reverse('authors:dashboard'))

    return render(request, 'pages/edit_obj_view.html', context={
        # 'remedio': remedio[0],
        'form': form,
        'form_button': 'Salvar',
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
        messages.success(request, "Remedio criado e enviado a analise")
        return redirect(reverse('authors:dashboard'))
    return render(request, 'pages/new_obj_view.html', context={
        'form': form,
        'form_button': 'Salvar',
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def delete_obj(request, idobject):
    if not request.POST:
        raise Http404
    remedio = models.Remedios.objects.get(id=idobject, is_published=False, author=request.user)
    titulo = remedio.title

    if remedio.delete():
        messages.success(request, f"{titulo} deletado!")
    else:
        messages.error(request, f"{titulo} não foi deletado!")

    return redirect(reverse('authors:dashboard'))
