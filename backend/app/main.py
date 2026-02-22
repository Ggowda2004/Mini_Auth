from fastapi import FastAPI


app=FastAPI()

@app.get("/")
def Home():
    return ("bullshit bro you dont know how to code")

"""
Auth-routes
POST /auth/register
POST /auth/login
GET  /auth/me   ← test your dependency

Apikey_routes
POST   /api-keys        → create key
GET    /api-keys        → list keys
DELETE /api-keys/{id}   → revoke key"""