import sqlite3

from schemas import UserCreate, UserLogin, UserRead, UserUpdate
from queries import Queries


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite.db")
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute(Queries.CREATE_USER_TABLE)

    def get_user_by_id(self, user_id: int) -> UserRead | None:
        self.cur.execute(Queries.GET_USER_BY_ID, {"id": user_id})
        row = self.cur.fetchone()
        if row:
            user = {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "username": row[4],
                "password": row[5],
            }
            return UserRead(**user)
        return None

    def get_user_by_username(self, username: str) -> UserLogin | None:
        self.cur.execute(Queries.GET_USER_BY_USERNAME, {"username": username})
        row = self.cur.fetchone()
        if row:
            user = {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "username": row[4],
                "password": row[5],
            }
            return UserLogin(**user)
        return None

    def get_user_by_email(self, email: str) -> UserRead | None:
        self.cur.execute(Queries.GET_USER_BY_EMAIL, {"email": email})
        row = self.cur.fetchone()
        if row:
            user = {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "username": row[4],
                "password": row[5],
            }
            return UserRead(**user)
        return None

    def get_all_users(self) -> list[UserRead]:
        self.cur.execute(Queries.GET_ALL_USERS)
        rows = self.cur.fetchall()
        return [
            UserRead(
                **{
                    "id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "email": row[3],
                    "username": row[4],
                    "password": row[5],
                }
            )
            for row in rows
        ]

    def create_user(self, user: UserCreate) -> UserRead | None:
        new_user = user.model_dump()
        self.cur.execute(Queries.CREATE_USER, new_user)
        self.conn.commit()
        return self.get_user_by_email(new_user["email"])

    def update_user(self, id: int, user: UserUpdate) -> UserRead | None:
        data = user.model_dump(exclude_none=True)
        if not data:
            return self.get_user_by_id(id)  # No hay campos para actualizar

        set_clause = ", ".join([f"{field} = :{field}" for field in data.keys()])
        query = f"UPDATE users SET {set_clause} WHERE id = :id"
        params = {**data, "id": id}
        self.cur.execute(query, params)
        self.conn.commit()
        return self.get_user_by_id(id)

    def delete_user(self, user_id: int):
        self.cur.execute(Queries.DELETE_USER, {"id": user_id})
        self.conn.commit()

    def close(self):
        self.conn.close()


tokens = {
    "token": "fake_jwt_token",
    "refresh_token": "fake_refresh_jwt_token",
    "new_token": "fake_new_jwt_token",
}
