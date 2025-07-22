from fastapi import HTTPException


class CredentialException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Could not validate credential",
            headers={"WWW-Authenticate": "Bearer"},
        )

class UserExistedCheck(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Email already existed !"
        )

class InvalidPassword(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid Password !"
        )

class InvalidUser(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Invalid User - User not found !"
        )

class BlacklistedToken(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Token has been revoked !"
        )

class PostNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Post not found !"
        )