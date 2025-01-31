from django.apps import AppConfig

class PointsWalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'points_wallet'

    def ready(self):
        import points_wallet.signals

