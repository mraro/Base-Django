import requests
from django.contrib import messages
from django.contrib.sessions.backends.base import SessionBase
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, CreateView
from django.views.generic.edit import BaseCreateView

from authors.forms import RegisterForm


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'pages/register_view.html'

    def get_context_data(self, **kwargs):
        session_data = self.request.session.get('register_form_data')
        # self.form_class = RegisterForm(session_data)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': RegisterForm(session_data),
            'form_action': reverse('authors:register_create'),
            'form_button': 'Cadastrar',
        })
        return context


class RegisterCreate(BaseCreateView):
    def get(self, *args):
        raise Http404()

    def post(self, request, *args, **kwargs):
        POST = request.POST  # Receive data by POST
        request.session['register_form_data'] = POST  # Give data from POST to SESSION
        form = RegisterForm(POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()
                messages.success(request, "Usuario Cadastrado com Sucesso!!!")
                del (request.session['register_form_data'])  # kill session
                return redirect('farmacia:home')
            except ValueError:
                messages.error(request, "Falha ao criar o usuario")
                return redirect('authors:register')

        return redirect('authors:register')

# class LoginView(BaseAuthorsView):
#     ...
