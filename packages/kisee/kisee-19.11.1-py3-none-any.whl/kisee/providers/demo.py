"""This is a really dumb identification backend: it does not store
anything and accepts almost any login/password pair.
"""
from typing import Optional

from kisee.identity_provider import IdentityProvider, User


class DemoBackend(IdentityProvider):
    """Dumb identity backend, for demo purposes.
    This backend follow the following rules:
     - Any user exist and have virtually all passwords.
     - Any password less or equal than 4 characters will fail.
     - root is a superuser.
    Yes, this mean than anybody logging as root with any password of
    more than 4 chars will be superuser. This is for demo purposes only.
    """

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    async def identify(self, login: str, password: str) -> Optional[User]:
        """Identifies the given login/password pair, returns a dict if found.
        """
        # pylint: disable=unused-argument
        if len(password) < 4:
            return None
        return User(
            user_id=login,
            username=login,
            email=f"{login}@example.com",
            is_superuser=login == "root",
        )

    async def register_user(
        self, username: str, password: str, email: str, is_superuser: bool = False
    ):
        pass

    async def get_user_by_email(self, email):
        """Get user with provided email address
        """
        return User(user_id=email, username=email, email=email)

    async def get_user_by_username(self, username):
        """Get user with provided username
        """
        return User(user_id=username, username=username, email=f"{username}@gmail.com")

    async def set_password_for_user(self, user: User, password: str):
        pass

    async def is_connection_alive(self) -> bool:
        """Verify that connection is alive, always return True
        """
        return True
