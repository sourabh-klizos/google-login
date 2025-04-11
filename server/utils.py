
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




@app.get('/auth/google/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    # print(await oauth.google.authorize_redirect(request, redirect_uri))
    # return {"login_url":await oauth.google.authorize_redirect(request, redirect_uri) }
    return await oauth.google.authorize_redirect(request, redirect_uri)





google = oauth.register(
    name='google',
    client_id='',
    client_secret='',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri = "https://www.googleapis.com/oauth2/v3/certs"
)








# @app.get('/auth/google/login')
# async def login(request: Request):
#     redirect_uri = request.url_for('auth')
#     return await oauth.google.authorize_redirect(request, redirect_uri)

















@app.get("/auth/google/callback")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)

    request.session["user"] = {
        "email": user["email"],
        "name": user["name"]
    }
    return RedirectResponse("http://localhost:5173/")