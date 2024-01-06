from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend

from settings import get_config
from db.models import UserModel
from schemas.users import LoginInput
from db.session import async_session_factory
from services.users import get_current_user, login_admin


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        data = LoginInput(email=username, password=password)
        try:
            async with async_session_factory.begin() as session:
                result = await login_admin(data, session)
                request.session.update(
                    {"token": f"{get_config().jwt.header} {result}"}
                )
                return True
        except Exception:
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        if not (token := request.session.get("token", None)):
            return RedirectResponse(
                request.url_for("admin:login"), status_code=302
            )
        try:
            async with async_session_factory.begin() as session:
                result = await get_current_user(
                    token=token.split()[-1], session=session
                )
            if isinstance(result, UserModel):
                request.session.update(
                    {
                        "user": {
                            "uuid": str(result.uuid),
                            "is_active": result.is_active,
                            "is_superuser": result.is_superuser,
                        }
                    }
                )
        except Exception:
            return False
        return True
