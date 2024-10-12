from django.apps import AppConfig


print('=======================')
print('core app')

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel.core'
    # name = 'core'
