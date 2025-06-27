from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token == "admin":
        return {"username": "admin", "role": "admin"}
    elif token == "user":
        return {"username": "user", "role": "user"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Neplatné prihlasovacie údaje",
        headers={"WWW-Authenticate": "Bearer"},
    )