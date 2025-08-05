from fastapi import HTTPException

#---------------------------------------------------------------#

####     HTTP CODE 400     #####

class UserExistedCheck(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Email already existed !"
        )

class SizeTooLarge(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="File size exceeds 20MB limit !"
        )

class EmptyQueryException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Search query can't be empty !"
        )

#---------------------------------------------------------------#

####     HTTP CODE 401     #####

class InvalidPassword(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid Password !"
        )

#---------------------------------------------------------------#

####     HTTP CODE 403     #####

class PermissionException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Permission Denied !"
        )

#---------------------------------------------------------------#

####     HTTP CODE 404     #####

class CredentialException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Could not validate credential",
            headers={"WWW-Authenticate": "Bearer"},
        )

class InvalidUser(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Invalid User - User not found !"
        )

class PostNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Post not found !"
        )

class DocumentNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Document not found !"
        )

#---------------------------------------------------------------#

####     HTTP CODE 500     #####

class FileUploadFailed(HTTPException):
    def __init__(self, detail="Upload File to AWS S3 Failed"):
        super().__init__(
            status_code=500,
            detail=detail
        )

class PresignedURLFailed(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=500,
            detail="Generate presigned URL failed !"
        )

#---------------------------------------------------------------#