from django.apps import AppConfig


class SchoolApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school_api'
    
    def ready(self):
        # هنا كنعيطو على signals باش يخدمو
        import school_api.signals


