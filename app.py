import asyncio
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

MAIN_BOT_TOKEN = "8383183638:AAGGTZY1QmCiRbYZZUHfPYPOjqDBOoRdH80"

bot = Bot(MAIN_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class SendMessage(StatesGroup):
    chat_id = State()
    token = State()
    text = State()


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.set_state(SendMessage.chat_id)
    await message.answer("Chat id bhej Bhai")


@dp.message(SendMessage.chat_id)
async def get_chatid(message: types.Message, state: FSMContext):
    await state.update_data(chat_id=message.text.strip())
    await state.set_state(SendMessage.token)
    await message.answer("Bot token bhej bhai")


@dp.message(SendMessage.token)
async def get_token(message: types.Message, state: FSMContext):
    await state.update_data(token=message.text.strip())
    await state.set_state(SendMessage.text)
    await message.answer("Text bhej Bhai")


@dp.message(SendMessage.text)
async def send_final(message: types.Message, state: FSMContext):
    data = await state.get_data()

    chat_id = data["chat_id"]
    token = data["token"]
    text = message.text

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:
        r = requests.post(url, data=payload)
        if r.status_code == 200:
            await message.answer("Message sent successfully ✅")
        else:
            await message.answer(f"Failed ❌\n{r.text}")
    except Exception as e:
        await message.answer(f"Error: {e}")

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
