
# @app.get("/auth/google/login")
# async def get_google_login_url(request: Request):
#     redirect_uri = request.url_for("auth")
#     redirect_url = await oauth.google.authorize_redirect(request, redirect_uri)
#     return JSONResponse(content={"login_url": redirect_url})



# @app.get("/auth/google/login")
# async def get_google_login_url(request: Request):
#     redirect_uri = request.url_for("auth")
#     client = oauth.create_client("google")
#     redirect_url = await client.authorize_redirect(request, redirect_uri)
#     print(redirect_url)
#     # return JSONResponse(content={"login_url": redirect_url})
#     return ""



# @app.get("/auth/google/login")
# async def get_google_login_url(request: Request):
#     try:

#         redirect_uri = request.url_for("auth")
#         # Generate the full Google OAuth URL
#         # redirect_url = await oauth.google.authorize_redirect_url(request, redirect_uri)
#         redirect_url =  await oauth.google.authorize_redirect(request, redirect_uri)
#         print(redirect_url)

#         return JSONResponse(content={"login_url": redirect_url})
#     except Exception as e:
#         print(e)




# @app.get('/auth/google/login')
# async def login(request: Request):
#     redirect_uri = request.url_for('auth')
#     # print(await oauth.google.authorize_redirect(request, redirect_uri))
#     # return {"login_url":await oauth.google.authorize_redirect(request, redirect_uri) }
#     return await oauth.google.authorize_redirect(request, redirect_uri)





# google = oauth.register(
#     name='google',
#     client_id='',
#     client_secret='',
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     api_base_url='https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
#     # This is only needed if using openId to fetch user info
#     client_kwargs={'scope': 'openid email profile'},
#     jwks_uri = "https://www.googleapis.com/oauth2/v3/certs"
# )








# # @app.get('/auth/google/login')
# # async def login(request: Request):
# #     redirect_uri = request.url_for('auth')
# #     return await oauth.google.authorize_redirect(request, redirect_uri)

















# @app.get("/auth/google/callback")
# async def auth(request: Request):
#     token = await oauth.google.authorize_access_token(request)
#     user = await oauth.google.parse_id_token(request, token)

#     request.session["user"] = {
#         "email": user["email"],
#         "name": user["name"]
#     }
#     return RedirectResponse("http://localhost:5173/")















###########################







CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/linkedin/callback"

LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_PROFILE_URL = "https://api.linkedin.com/v2/me"
LINKEDIN_EMAIL_URL = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"


print(CLIENT_ID)

@app.get("/auth/linkedin")
def linkedin_login():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "state": "random_string_123",
    }
    url = f"{LINKEDIN_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url)







@app.get("/auth/linkedin/callback")
async def linkedin_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return JSONResponse({"error": "No code found in request"}, status_code=400)

    async with httpx.AsyncClient() as client:
        # Exchange code for access token
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
        access_token = token_data.get("access_token")
        if not access_token:
            return JSONResponse({"error": "Failed to obtain access token"}, status_code=400)

        # Fetch LinkedIn profile
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_res = await client.get(LINKEDIN_PROFILE_URL, headers=headers)
        email_res = await client.get(LINKEDIN_EMAIL_URL, headers=headers)

        return {
            "profile": profile_res.json(),
            "email": email_res.json()
        }


# @app.get("/auth/linkedin/callback")
# async def linkedin_callback(request: Request):
#     print("Query Params:", dict(request.query_params))

#     error = request.query_params.get("error")
#     if error:
#         return JSONResponse({"error": error}, status_code=400)

#     code = request.query_params.get("code")
#     if not code:
#         return JSONResponse({"error": "No code found in request"}, status_code=400)