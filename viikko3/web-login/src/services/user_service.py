from entities.user import User
import re
from repositories.user_repository import (
    user_repository as default_user_repository
)


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password, password_confirmation):
        self.validate(username, password, password_confirmation)

        user = self._user_repository.create(
            User(username, password)
        )

        return user

    def validate(self, username, password, password_confirmation):
        if not username or not password:
            raise UserInputError("Username and password are required")

        if not password_confirmation:
            raise UserInputError("Password confirmation is required.")

        # username validation
        if not re.match("^[a-z]{3,}$", username):
            raise UserInputError(
                "Invalid username. Username must be at least 3 characters long and consist of letters a-z")

        existing = self._user_repository.find_by_username(username)
        if existing:
            raise UserInputError("Username is already taken")

        # password validation
        if password.isalpha() or len(password) < 8:
            raise UserInputError(
                "Invalid password. Password must be at least 8 characters long and not consist of only letters.")

        if password != password_confirmation:
            raise UserInputError(
                "Password confirmation didn't match the password.")


user_service = UserService()
