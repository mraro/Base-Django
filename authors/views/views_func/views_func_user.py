from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _

from authors.forms import RegisterForm, LoginForm, EditObjectForm


# Create your views here. # FUNC BASE TO VIEWS
def register_view(request):  # request is raw information that comes from browser
    session_data = request.session.get('register_form_data',
                                       None)  # Default None # session is a data that keeps after reload the page
    form = RegisterForm(session_data)  # this is a form created at forms folder( I put some examples there but has
    # more in documentation django)

    return render(request, 'pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
        'form_button': _('Register'),
    })


def register_create(request):
    if not request.POST:  # Avoid "pilantras" to send get data and crash site
        raise Http404()

    POST = request.POST  # Receive data by POST
    request.session['register_form_data'] = POST  # Give data from POST to SESSION
    form = RegisterForm(POST)

    if form.is_valid():  # form valid is important to be able to form.save
        try:
            user = form.save(commit=False)  # receive data from form, after valid but don't save yet
            user.set_password(user.password)  # cryptography password
            user.save()  # save data in DB
            messages.success(request, _("User registered successfully!!!"))

            del (request.session['register_form_data'])  # kill session
            return redirect('farmacia:home')
        except ValueError:
            messages.error(request, _("Fail in create user"))
            return redirect('authors:register')

    return redirect('authors:register')


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

    if form.is_valid():
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
            messages.error(request, _('User and/or password wrong'))
            return redirect(login_page)

    messages.error(request, _('fill the fields properly'))

    return redirect(login_page)


# @login_required(login_url='authors:login', redirect_field_name='next')
def logout_backend(request):
    if not request.POST:
        raise Http404
    # print(request.POST.get('username'), ' >< ', request.user.username)
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    see_you = _('See you')
    logout(request)
    if request.POST.get('first_name'):
        messages.success(request, f"{see_you} {request.POST.get('first_name')}")
    else:
        messages.success(request, f"{see_you} {request.POST.get('username')}")

    return redirect(reverse('farmacia:home'))