from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.responses import JSONResponse
import os
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse

load_dotenv()


print(os.getenv("GOOGLE_REDIRECT_URI"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="keyrgjnhjbhghjvnhgibigubhmijhbyiowuybhoiq4v")

oauth = OAuth()
oauth.register(
    name='google',
    # client_kwargs={
    #     'scope': 'openid email profile'
    # },
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid email profile'},
    redirect_uri=os.getenv("GOOGLE_REDIRECT_URI"),
    jwks_uri = "https://www.googleapis.com/oauth2/v3/certs",
    
    userinfo_endpoint='https://www.googleapis.com/oauth2/v2/userinfo'

)












@app.get("/auth/google/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")  
    print("Redirect URI:", redirect_uri)  

    return  await oauth.google.authorize_redirect(request,redirect_uri)


# http://localhost:8000/auth/google/callback
# @app.get('/auth/google/callback')
# async def auth(request: Request):
#     try:

#         token = await oauth.google.authorize_access_token(request)
#         user = await oauth.google.parse_id_token(request, token)
#         print(token) 
#         print(user)
#         return {"email": user['email'], "name": user['name']}
#     except Exception as e:
#         print(e)
#         return {"error": str(e)}

@app.get('/auth/google/callback')
async def auth(request: Request):
    try:
        # 1. Exchange code for token
        token = await oauth.google.authorize_access_token(request)

        # 2. Get user info from ID token or Google API
        user_info = await oauth.google.parse_id_token(request, token)
        # OR
        # user_info = await oauth.google.get('userinfo', token=token)

        # You can now save token in session or DB, etc.
        return JSONResponse(content={
            "access_token": token.get("access_token"),
            "id_token": token.get("id_token"),
            "user_info": user_info
        })
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})