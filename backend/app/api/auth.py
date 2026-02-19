from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from app.db.session import get_db
from app.db import models
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth.deps import get_current_user

router = APIRouter()

@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    if os.getenv("ALLOW_REGISTER", "1") != "1":
        raise HTTPException(status_code=403, detail="Registration disabled")
    if db.query(models.User).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="User exists")
    user = models.User(email=email, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    return {"ok": True}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.id})
    return {"access_token": token}

@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"id": user.id, "email": user.email}
