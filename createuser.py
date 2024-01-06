import sys
import asyncio
from getpass import getpass

from dao.users import UserDAO
from db.models import UserModel
from utils.auth import get_password_hash
from db.session import async_session_factory

email = input("Email: ")


async def async_main() -> None:
    async with async_session_factory.begin() as session:
        if await UserDAO(session).get(email=email):
            sys.stdout.write("User already exists\n")
        else:
            user = UserModel(email=email)
            password = getpass()
            user.hashed_password = get_password_hash(password)
            user.is_superuser = True
            user.is_active = True
            session.add(user)
            sys.stdout.write("User was successfully created\n")
            await session.commit()


asyncio.run(async_main())
