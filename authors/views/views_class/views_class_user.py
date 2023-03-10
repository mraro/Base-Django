from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
from django.views.generic.edit import BaseCreateView, ProcessFormView

from authors.forms import RegisterForm, LoginForm

"""
- LoginView - exibe um formulário de login e processa os dados de entrada
- LogoutView - encerra a sessão do usuário e redireciona para outra URL
- PasswordChangeView - exibe um formulário para alterar a senha do usuário e processa os dados de entrada
- PasswordResetView - exibe um formulário para redefinir a senha do usuário e processa os dados de entrada
- PasswordResetConfirmView - exibe um formulário para confirmar a redefinição da senha do usuário e processa os dados de entrada

- TemplateView - exibe um único template
- ListView - exibe um conjunto de objetos em um template
- DetailView - exibe detalhes de um objeto específico em um template
- FormView - exibe um formulário e processa dados de entrada
- CreateView - exibe um formulário para criar um novo objeto e processa os dados de entrada
- UpdateView - exibe um formulário para atualizar um objeto existente e processa os dados de entrada
- DeleteView - exibe um formulário para excluir um objeto existente e processa os dados de entrada

- RedirectView - redireciona o usuário para outra URL
- ArchiveIndexView - exibe um índice de objetos arquivados
- YearArchiveView - exibe um índice de objetos arquivados por ano
- MonthArchiveView - exibe um índice de objetos arquivados por mês
- DayArchiveView - exibe um índice de objetos arquivados por dia
- DateDetailView - exibe detalhes de um objeto arquivado específico
- WeekArchiveView - exibe um índice de objetos arquivados por semana
- TodayArchiveView - exibe um índice de objetos arquivados para o dia atual
""" # noqa


class Register_View(FormView):
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


class Register_Create(BaseCreateView):
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


class Login_View(FormView):
    form_class = LoginForm
    template_name = 'pages/login_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_action': reverse('authors:authenticate'),
            'form_button': 'Login',
        })
        return context


class Login_Authenticate(ProcessFormView):

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        POST = request.POST  # Recive data by POST
        # print("\n ", POST, "\n")
        form = LoginForm(POST)

        if form.is_valid():
            user_authenticate = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )

            if user_authenticate is not None:
                login(request, user_authenticate)
                messages.success(request, "Sucesso no Login!")
                return redirect(reverse('farmacia:home'))

            else:
                messages.error(request, 'Usuario e/ou senha incorretos')
                return redirect(reverse('authors:login'))

        messages.error(request, 'preencha os campos corretamente')
        return redirect(reverse('authors:login'))


class Logout_Backend(LogoutView):
    http_method_names = ['post', ]
    get = Http404

    def post(self, request, *args, **kwargs):
        if request.POST.get('username') != request.user.username:
            return redirect(reverse('authors:login'))

        logout(request)
        if request.POST.get('first_name'):
            messages.success(request, f"Até mais {request.POST.get('first_name')}")
        else:
            messages.success(request, f"Até mais {request.POST.get('username')}")

        return redirect(reverse('farmacia:home'))
