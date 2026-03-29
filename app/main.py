from fastapi import FastAPI, HTTPException, status
from app.database.database import tokens
from app.routes.users import router as users_router

app = FastAPI()

app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/test-valid-user")
async def test_valid_user(data: dict[str, str]) -> dict[str, str]:
    if data["token"] == tokens["token"] or data["token"] == tokens["new_token"]:
        return {"message": "user can access this resource"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token."
        )
