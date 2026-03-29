from fastapi import APIRouter, HTTPException, status
from app.database.database import Database, tokens
from app.schemas.schemas import UserCreate, UserLogin, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

db = Database()


@router.post("/login")
async def login(credentials: UserLogin) -> dict[str, str]:
    cred = credentials.model_dump()
    username = cred["username"]
    password = cred["password"]
    user = db.get_user_by_username(username)
    if not user or user.username != username or user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials."
        )
    return {
        "message": "Login successful.",
        "token": tokens["token"],
        "refresh_token": tokens["refresh_token"],
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(new_user: UserCreate) -> UserRead | None:
    check_user = new_user.model_dump()
    check_existing_username = db.get_user_by_username(check_user["username"])
    check_existing_email = db.get_user_by_email(check_user["email"])
    if check_existing_username or check_existing_email:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Username or email already exists.",
        )
    user = db.create_user(new_user)
    return user


@router.get("/")
async def get_users() -> list[UserRead]:
    return db.get_all_users()


@router.get("/{user_id}")
async def get_user(user_id: int) -> UserRead:
    user = db.get_user_by_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@router.delete("/{user_id}")
async def delete_user(user_id: int) -> dict[str, str]:
    db.delete_user(user_id)
    return {"message": f"User with id {user_id} deleted successfully."}


@router.put("/{user_id}")
async def update_user(user_id: int, updated_user: UserUpdate) -> UserRead | None:
    user = db.update_user(id=user_id, user=updated_user)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@router.put("/refresh")
async def refresh_token(refresh_token: str) -> str:
    if refresh_token == tokens["refresh_token"]:
        return tokens["new_token"]
    else:
        return ""


@router.get("/logout")
async def logout() -> dict[str, str]:
    return {"token": "invalid_token", "message": "Logged out successfully."}
