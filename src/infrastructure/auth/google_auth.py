
from src.main.config.settings import GoogleAuthSettings
from authlib.integrations.starlette_client import OAuth




def get_google_auth_obj(google_auth_settings: GoogleAuthSettings) -> OAuth:
    """Get the google auth obj engine instance."""
    # prepare the engine
    auth_obj = google_auth_settings.google_auth_object()

    return auth_obj