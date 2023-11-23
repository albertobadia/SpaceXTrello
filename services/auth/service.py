import datetime

from jose import jwt
from passlib.context import CryptContext

from api.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    A service used to handle authentication related tasks.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes the given password using the bcrypt algorithm.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain text password against a hashed password.

        Args:
            plain_password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the plain text password matches the hashed password, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        data: dict, expires_delta: datetime.timedelta | None = None
    ):
        """
        Create an access token for the given data.

        Args:
            data (dict): The data to be encoded in the token.
            expires_delta (datetime.timedelta | None): Optional expiration time for the token.

        Returns:
            bytes: The encoded access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
