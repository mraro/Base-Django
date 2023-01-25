from django.core.checks import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegisterForm


# Create your views here.
def register_view(request):
    session_data = request.session.get('register_form_data', None)  # Default None
    form = RegisterForm(session_data)

    return render(request, 'pages/register_view.html', {
        'form': form,

    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST  # Recive data by POST
    request.session['register_form_data'] = POST  # Give data from POST to SESSION
    form = RegisterForm(POST)
    if form.is_valid:
        try:
            form.save()
            messages.success(request, "Usuario Cadastrado com Sucesso!!!")
            del (request.session['register_form_data'])
            return redirect('farmacia:home')
        except ValueError:
            messages.error(request, "Falha ao criar o usuario")
            return redirect('authors:register')

    return redirect('authors:register')
