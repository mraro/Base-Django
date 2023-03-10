from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authors"

    # ISSO É ESTA LENDO OQUE ACONTECE QUANDO SALVA UM USUARIO E SE QUISER POSSO PEGAR INFORMAÇÕES E EDITALAS CHAMANDO A # noqa
    # FUNÇÃO AQUI   # noqa
    def ready(self, *args, **kwargs) -> None:
        import authors.signals
        super_ready = super().ready(*args, **kwargs)
        return super_ready
