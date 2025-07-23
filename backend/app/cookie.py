from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import timedelta
from fastapi import Request

auth = APIRouter(prefix="/auth", tags=["auth"])

@auth.post("/login")
async def login():
    # do your auth, get session_id or JWT
    token = "some-signed-token"
    resp = JSONResponse({"ok": True})
    resp.set_cookie(
        key="session",
        value=token,
        httponly=True,          # JS can't read it → safer
        secure=False,           # True in production (HTTPS)
        samesite="lax",         # "none" if cross-site; then secure must be True
        max_age=int(timedelta(days=7).total_seconds()),
        path="/"
    )
    return resp

@auth.post("/logout")
async def logout():
    resp = JSONResponse({"ok": True})
    resp.delete_cookie("session")
    return resp

@auth.get("/me")
async def me(request: Request):
    token = request.cookies.get("session")
    # validate token / load user
    return {"token": token}

