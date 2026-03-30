from fastapi import APIRouter, HTTPException, status
from app.database.database import tokens
from app.schemas.schemas import UserCreate, UserLogin, UserRead, UserUpdate
from app.services.auth import authenticate_user
import app.services.users as users_service


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users() -> list[UserRead]:
    return users_service.get_all_users()


@router.get("/{user_id}")
async def get_user(user_id: int) -> UserRead:
    user = users_service.get_user_by_id(user_id)
    if user:
        return UserRead(**user.model_dump())
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@router.delete("/{user_id}")
async def delete_user(user_id: int) -> dict[str, str]:
    if not users_service.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return {"message": f"User with id {user_id} successfully deleted."}


@router.put("/{user_id}")
async def update_user(user_id: int, updated_user: UserUpdate) -> UserRead | None:
    user = users_service.update_user(user_id, updated_user)
    if user:
        return UserRead(**user.model_dump())
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(new_user: UserCreate) -> UserRead | None:
    if users_service.verify_user_exists(new_user):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Username or email already exists.",
        )
    user = users_service.create_user(new_user)
    return UserRead(**user.model_dump())


@router.post("/login")
async def login(credentials: UserLogin) -> dict[str, str]:
    if not authenticate_user(credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials."
        )
    return {
        "message": "Login successful.",
        "token": tokens["token"],
        "refresh_token": tokens["refresh_token"],
    }


@router.get("/logout")
async def logout() -> dict[str, str]:
    return {"token": "invalid_token", "message": "Logged out successfully."}


@router.put("/refresh")
async def refresh_token(refresh_token: str) -> str:
    if refresh_token == tokens["refresh_token"]:
        return tokens["new_token"]
    else:
        return ""
