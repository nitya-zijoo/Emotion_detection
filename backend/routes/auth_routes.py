from fastapi import APIRouter
from pydantic import BaseModel
from backend.firebase_auth import register_user, login_user, send_verification_email, get_user_info
from database import save_user

router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    age_group: str
    gender: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(request: RegisterRequest):
    result = register_user(request.email, request.password)
    if "error" in result:
        return {"error": result["error"]["message"]}
    
    uid = result["localId"]
    id_token = result["idToken"]
    
    save_user(uid, request.email, request.name, request.age_group, request.gender)
    send_verification_email(id_token)
    
    return {
        "uid": uid,
        "email": request.email,
        "name": request.name,
        "message": "Registered successfully. Verification email sent."
    }

@router.post("/login")
def login(request: LoginRequest):
    result = login_user(request.email, request.password)
    if "error" in result:
        return {"error": result["error"]["message"]}
    
    user_info = get_user_info(result["idToken"])
    
    return {
        "uid": result["localId"],
        "id_token": result["idToken"],
        "email": result["email"],
        "email_verified": user_info.get("emailVerified", False),
        "message": "Login successful."
    }
