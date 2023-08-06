from typing import Callable, Type

from fastapi_users.authentication import BaseAuthentication
from fastapi_users.db import BaseUserDatabase
from fastapi_users.models import BaseUser, BaseUserDB
from fastapi_users.router import Event, UserRouter, get_user_router


class FastAPIUsers:
    """
    Main object that ties together the component for users authentication.

    :param db: Database adapter instance.
    :param auth: Authentication logic instance.
    :param user_model: Pydantic model of a user.
    :param reset_password_token_secret: Secret to encode reset password token.
    :param reset_password_token_lifetime_seconds: Lifetime of reset password token.

    :attribute router: Router exposing authentication routes.
    :attribute get_current_user: Dependency callable to inject authenticated user.
    """

    db: BaseUserDatabase
    auth: BaseAuthentication
    router: UserRouter
    get_current_user: Callable[..., BaseUserDB]

    def __init__(
        self,
        db: BaseUserDatabase,
        auth: BaseAuthentication,
        user_model: Type[BaseUser],
        reset_password_token_secret: str,
        reset_password_token_lifetime_seconds: int = 3600,
    ):
        self.db = db
        self.auth = auth
        self.router = get_user_router(
            self.db,
            user_model,
            self.auth,
            reset_password_token_secret,
            reset_password_token_lifetime_seconds,
        )

        get_current_user = self.auth.get_current_user(self.db)
        self.get_current_user = get_current_user  # type: ignore

        get_current_active_user = self.auth.get_current_active_user(self.db)
        self.get_current_active_user = get_current_active_user  # type: ignore

        get_current_superuser = self.auth.get_current_superuser(self.db)
        self.get_current_superuser = get_current_superuser  # type: ignore

    def on_after_register(self) -> Callable:
        """Add an event handler on successful registration."""
        return self._on_event(Event.ON_AFTER_REGISTER)

    def on_after_forgot_password(self) -> Callable:
        """Add an event handler on successful forgot password request."""
        return self._on_event(Event.ON_AFTER_FORGOT_PASSWORD)

    def _on_event(self, event_type: Event) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.router.add_event_handler(event_type, func)
            return func

        return decorator
