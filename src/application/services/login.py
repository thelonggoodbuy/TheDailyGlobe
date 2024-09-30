import json
from fastapi import FastAPI
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi.responses import JSONResponse


class LoginGmailService(ILoginService):
     async def check_login_data(self, request: Request):
        redirect_uri = request.url_for('auth')
        auth_url = await oauth.google.create_authorization_url(redirect_uri.__dict__['_url'])
        await oauth.google.save_authorize_data(request, redirect_uri=str(redirect_uri), **auth_url)
        return JSONResponse(content=auth_url)