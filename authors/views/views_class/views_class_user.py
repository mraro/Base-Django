from django.views.generic import FormView


class BaseAuthorsView(FormView):
    pass


class RegisterView(BaseAuthorsView):
    ...


class LoginView(BaseAuthorsView):
    ...

