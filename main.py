import json
from typing import Any

from fastapi import FastAPI, HTTPException, status
from database import users, tokens

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login")
async def login(credentials: dict[str, str]) -> dict[str, str]:
    username = credentials["username"]
    password = credentials["password"]
    for user in users:
        if user["username"] == username and user["password"] == password:
            return {
                "message": "Login successful.",
                "token": tokens["token"],
                "refresh_token": tokens["refresh_token"],
            }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials."
    )


@app.post("/register")
async def register_user(new_user: dict[str, str]) -> dict[str, int]:
    # validate user input
    if (
        not new_user["first_name"]
        or not new_user["last_name"]
        or not new_user["email"]
        or not new_user["username"]
        or not new_user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or incomplete data for registering.",
        )
    else:
        ids = [user["id"] for user in users]
        new_id = max(ids) + 1 if ids else 1
        new_user["id"] = new_id
        users.append(new_user)
        return {"id": new_id}


@app.get("/users")
async def get_users() -> list[dict[str, Any]]:
    return users


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> dict[str, Any]:
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@app.delete("/users/{user_id}")
async def delete_user(user_id: int) -> dict[str, str]:
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return {"message": "User deleted successfully."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@app.put("/users/{user_id}")
async def update_user(user_id: int, updated_user: dict[str, str]) -> dict[str, str]:
    for user in users:
        if user["id"] == user_id:
            user.update(updated_user)
            return {"message": "User updated successfully."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@app.put("/refresh")
async def refresh_token(refresh_token: str) -> str:
    if refresh_token == tokens["refresh_token"]:
        return tokens["new_token"]
    else:
        return ""


@app.get("/logout")
async def logout() -> dict[str, str]:
    return {"token": "invalid_token", "message": "Logged out successfully."}


@app.post("/test-valid-user")
async def test_valid_user(data: dict[str, str]) -> dict[str, str]:
    if data["token"] == tokens["token"] or data["token"] == tokens["new_token"]:
        return {"message": "user can access this resource"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token."
        )
