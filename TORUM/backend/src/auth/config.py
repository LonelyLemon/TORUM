from ..config import get_settings

settings = get_settings()

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXPIRATION_HOURS = settings.JWT_EXPIRATION_HOURS
REFRESH_TOKEN_HOURS = settings.REFRESH_TOKEN_HOURS