from django.apps import AppConfig


class FarmaciaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "farmacia"

    def ready(self, *args, **kwargs):
        import farmacia.signals  # noqa
        super_ready = super().ready(*args, **kwargs)  # noqa
        return super_ready
