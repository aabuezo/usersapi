from app.schemas.schemas import UserLogin
from app.services.security import verify_password
from app.services.users import get_user_credentials


def authenticate_user(credentials: UserLogin) -> bool:
    user_cred = credentials.model_dump()
    user = get_user_credentials(user_cred["username"])
    if user:
        user_data = user.model_dump()
        if verify_password(user_cred["password"], user_data["password"]):
            return True
    return False
