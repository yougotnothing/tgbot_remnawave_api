import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI
from remnawave import RemnawaveSDK
from remnawave.models.subscription import UserResponseDto
from remnawave.models.users import (
    CreateUserRequestDto,
    UpdateUserRequestDto,
)

load_dotenv()

app = FastAPI()
remnawave = RemnawaveSDK(
    base_url=os.getenv("REMNAWAVE_BASE_URL"),
    token=os.getenv("REMNAWAVE_TOKEN"),
)


@app.get("/user/{user_id}")
async def get_user(user_id: str):
    return await remnawave.users.get_user_by_username(user_id)


@app.post("/user")
async def create_user(data: CreateUserRequestDto):
    return await remnawave.users.create_user(data)


@app.patch("/user/{user_id}")
async def update_user(user_id: str, data: UpdateUserRequestDto):
    user = await remnawave.users.get_user_by_username(user_id)
    dicted_data = data.model_dump()

    expire_at = datetime.fromisoformat(dicted_data["expire_at"])

    if user is UserResponseDto:
        result = await remnawave.users.update_user(
            body=UpdateUserRequestDto(expire_at=expire_at, **dicted_data)
        )
        return {"data": result}


@app.delete("/user/{user_id}")
async def delete_user(user_id: str):
    user = await remnawave.users.get_user_by_username(user_id)

    if user is UserResponseDto:
        return await remnawave.users.delete_user(user.uuid)
