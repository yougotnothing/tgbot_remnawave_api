import os

import httpx
from fastapi import FastAPI
from remnawave import RemnawaveSDK
from remnawave.models.users import (
    CreateUserRequestDto,
    UpdateUserRequestDto,
)

app = FastAPI()
client = httpx.AsyncClient(
    base_url=os.getenv("REMNAWAVE_BASE_URL"),
    headers={"Authorization": f"Bearer {os.getenv('REMNAWAVE_TOKEN')}"},
)
remnawave = RemnawaveSDK(client=client)


@app.get("/user/{user_id}")
async def get_user(user_id: str):
    return await remnawave.users.get_user_by_username(user_id)


@app.post("/user")
async def create_user(data: CreateUserRequestDto):
    return await remnawave.users.create_user(data)


@app.patch("/user/{user_id}")
async def update_user(user_id: str, data: UpdateUserRequestDto):
    user = await remnawave.users.get_user_by_username(user_id)
    return await remnawave.users.update_user(uuid=user.uuid, *data)


@app.delete("/user/{user_id}")
async def delete_user(user_id: str):
    user = await remnawave.users.get_user_by_username(user_id)
    return await remnawave.users.delete_user(user.uuid)
