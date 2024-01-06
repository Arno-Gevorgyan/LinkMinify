from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from api import api_router
from settings import get_config
from db.models import UserModel
from permissions import is_admin
from admin import init_admin_page
from admin.base import CustomAdmin
from auth_backend import AdminAuth
from schemas.users import LoginInput
from services.users import login_admin
from exceptions import NotAuthenticated
from db.session import Engine, get_async_session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_origins=["*"],
    allow_methods=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=get_config().jwt.secret)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


engine = Engine.get()
auth_backend = AdminAuth(secret_key=get_config().jwt.secret)
admin_app = CustomAdmin(
    app=app,
    engine=engine,
    title="Link Minify Admin",
    authentication_backend=auth_backend,
)
init_admin_page(admin_app)


app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "templates"),
    name="static",
)

templates = Jinja2Templates(directory="templates")


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/info")
async def info(current_user: UserModel = Depends(is_admin)) -> dict:
    """Getting app info"""
    if current_user.is_active and current_user.is_superuser:
        return get_config().dict()
    return {
        "app_name": get_config().app.app_name,
        "admin_email": get_config().app.admin_email,
    }


@app.post("/token", include_in_schema=False)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Getting token for docs"""

    cred = LoginInput(
        email=form_data.username,
        password=form_data.password,
    )
    try:
        data = await login_admin(cred, session)
    except Exception as e:
        raise NotAuthenticated from e

    return {"access_token": data, "token_type": get_config().jwt.header}


app.include_router(api_router.router)
