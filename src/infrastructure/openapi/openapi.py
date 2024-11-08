from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer


bearer_scheme = HTTPBearer()
bearer_scheme_for_pages_with_unregistered_users = HTTPBearer(auto_error=False)