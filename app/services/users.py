from app.database.database import Database
from app.schemas.schemas import UserCreate, UserLogin, UserRead, UserUpdate
from app.services.security import hash_password


def verify_user_exists(user: UserCreate) -> bool:
    user = user.model_dump()
    with Database() as db:
        user_checked = db.get_user_by_username(user["username"])
    existing_user = user_checked.model_dump() if user_checked else None
    if existing_user and (
        existing_user["username"] == user["username"]
        or existing_user["email"] == user["email"]
    ):
        return True
    return False


def create_user(new_user: UserCreate) -> UserRead:
    user = new_user.model_dump()
    user["password"] = hash_password(user["password"])
    with Database() as db:
        return db.create_user(UserCreate(**user))


def update_user(user_id: int, updated_user: UserUpdate) -> UserRead | None:
    user_data = updated_user.model_dump(exclude_none=True)
    if "password" in user_data:
        user_data["password"] = hash_password(user_data["password"])
    with Database() as db:
        return db.update_user(id=user_id, user=UserUpdate(**user_data))


def get_all_users() -> list[UserRead]:
    with Database() as db:
        return db.get_all_users()


def get_user_by_id(user_id: int) -> UserRead | None:
    with Database() as db:
        return db.get_user_by_id(user_id)


def get_user_credentials(username: str) -> UserLogin:
    with Database() as db:
        return db.get_user_credentials(username)


def delete_user(user_id: int) -> bool:
    with Database() as db:
        return db.delete_user(user_id)
