from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from api.routes.query import router as queryRouter
from api.routes.upload import router as uploadRouter
from core.auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

app = FastAPI()

app.include_router(queryRouter, prefix="/query", tags=["Query"])
app.include_router(uploadRouter, prefix="/upload", tags=["Upload"])

@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires,
    )
    return {"access_token": token, "token_type": "bearer"}


@app.get("/")
def root():
    return {"message": "Base Endpoint of the application"}
