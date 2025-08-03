from fastapi import HTTPException


class CredentialException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Could not validate credential",
            headers={"WWW-Authenticate": "Bearer"},
        )

class PermissionException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Permission Denied !"
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

class FileUploadFailed(HTTPException):
    def __init__(self, detail="Upload File to AWS S3 Failed"):
        super().__init__(
            status_code=500,
            detail=detail
        )

class DocumentNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Document not found !"
        )

class PresignedURLFailed(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=500,
            detail="Generate presigned URL failed !"
        )