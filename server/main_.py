from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()



app = FastAPI()



# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="sourabh123test")

print(os.getenv("GOOGLE_CLIENT_ID"))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid email profile'},
    # redirect_uri=os.getenv("GOOGLE_REDIRECT_URI"),
    jwks_uri = "https://www.googleapis.com/oauth2/v3/certs",
    
    userinfo_endpoint='https://www.googleapis.com/oauth2/v2/userinfo'

)



@app.get('/auth/google/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get('/auth/google/callback')
async def auth(request: Request):
    try:

        token = await oauth.google.authorize_access_token(request)
        print("token " ,token)
        user_info = token.get('userinfo')
        response = {}
        if user_info:
            response['user'] = user_info
        if token:
            response['token'] = token
        
        if response:
            return response
        return {'error': 'Failed to retrieve user information'}
    except Exception as e:
        return {'error': str(e)}
        
