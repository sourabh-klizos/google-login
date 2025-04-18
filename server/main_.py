from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse , JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import httpx
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
        





CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/linkedin/callback"

LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"


USERINFO_URL = "https://api.linkedin.com/v2/userinfo"


@app.get("/auth/linkedin")
def linkedin_login():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email", #   "scope": "r_liteprofile r_emailaddress",   <- this breaks url
        # "state": "random_string_123",
    }
    url = f"{LINKEDIN_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url)



@app.get("/auth/linkedin/callback")
async def linkedin_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return JSONResponse({"error": "No code found in request"}, status_code=400)

    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            LINKEDIN_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        token_data = token_res.json()

        # print(token_data)
        access_token = token_data.get("access_token")
        if not access_token:
            return JSONResponse({"error": "Failed to obtain access token"}, status_code=400)


        headers = {"Authorization": f"Bearer {access_token}"}
        details = await client.get(USERINFO_URL, headers=headers)
      

        # print(details)
      

        return {
            "details": details.json(),
            "token_data" : token_data
        }
