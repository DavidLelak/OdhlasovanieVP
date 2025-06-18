from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Príklad: pevne definovaní používatelia
fake_users_db = {
    "admin": {"username": "admin", "role": "admin"},
    "worker": {"username": "worker", "role": "worker"},
}

# Hlavná autentifikačná funkcia
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_users_db.get(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Voliteľne: router pre /login endpoint
router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or form_data.password != form_data.username:
        # heslo = používateľské meno (len na demonštráciu)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return {"access_token": form_data.username, "token_type": "bearer"}
