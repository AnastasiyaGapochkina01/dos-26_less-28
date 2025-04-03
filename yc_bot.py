#!/usr/bin/python3
import asyncio
import os
import json
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# YC
YC_TOKEN = os.getenv('YC_TOKEN')
FOLDER_ID = os.getenv('YC_FOLDER_ID')

# TG
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

headers = {
    'Authorization': f'Bearer {YC_TOKEN}',
}

def find_vm(vm_name):
    url = f'https://compute.api.cloud.yandex.net/compute/v1/instances?folderId={FOLDER_ID}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        instances = response.json().get('instances', [])

        for instance in instances:
            name = instance.get('name')
            labels = instance.get('labels', {})
            instanceId = instance.get('id')
            if vm_name == name:
                return instanceId



@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("/list - список ВМ\n/run <vm-name> - запустить ВМ")


@dp.message(Command("list"))
async def vms_list(message: Message):
    url = f'https://compute.api.cloud.yandex.net/compute/v1/instances?folderId={FOLDER_ID}'
    #instances = {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        instances = response.json().get('instances', [])
        vm_list = "Список виртуальных машин:\n\n"
        for instance in instances:
            name = instance.get('name')
            state = instance.get('status')
            vm_list += f"name: {name}\n"
            vm_list += f"state: {state}\n-----------------\n"
        await message.answer(vm_list)
    else:
        print(f"Error: {response.text} - {response.status_code}")


@dp.message(Command("run"))
async def start_vm(message: Message):
    vm_name = message.text.split(maxsplit=1)[1]
    instanceId = find_vm(vm_name)
    url = f'https://compute.api.cloud.yandex.net/compute/v1/instances/{instanceId}:start'
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        await message.answer(f'{vm_name} starting...')
    else:
        await message.answer(f'Something wrong')


@dp.message(Command("stop"))
async def stop_vm(message: Message):
    vm_name = message.text.split(maxsplit=1)[1]
    instanceId = find_vm(vm_name)
    url = f'https://compute.api.cloud.yandex.net/compute/v1/instances/{instanceId}:stop'
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        await message.answer(f"{vm_name} stopping...")
    else:
        await message.answer(f"Something wrong")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
