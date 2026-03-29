class Queries:
    CREATE_USER_TABLE = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """

    GET_USER_BY_ID = """
        SELECT * FROM users WHERE id = :id
    """

    GET_USER_BY_USERNAME = """
        SELECT * FROM users WHERE username = :username
    """

    GET_USER_BY_EMAIL = """
        SELECT * FROM users WHERE email = :email
    """

    GET_ALL_USERS = """
        SELECT * FROM users
    """

    CREATE_USER = """
        INSERT INTO users (first_name, last_name, email, username, password)
        VALUES (:first_name, :last_name, :email, :username, :password)
    """

    UPDATE_USER = """
        UPDATE users SET 
        first_name = :first_name, 
        last_name = :last_name, 
        email = :email, 
        username = :username, 
        password = :password
        WHERE id = :id
    """

    DELETE_USER = """
        DELETE FROM users WHERE id = :id
    """
