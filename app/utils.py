from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #set hashing algo

def hash_pwd(password: str) -> str:
    return pwd_context.hash(password)