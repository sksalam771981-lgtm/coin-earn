from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import asyncio
import random
import string

from config import BOT_TOKEN, ADMIN_ID
from database import save_video, get_video

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


def generate_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@dp.message(F.video)
async def upload_video(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    file_id = message.video.file_id
    code = generate_code()

    save_video(code, file_id)

    link = f"https://t.me/{(await bot.get_me()).username}?start={code}"

    await message.answer(
        f"✅ ভিডিও সংরক্ষণ হয়েছে!\n\n🔗 Link:\n{link}"
    )@dp.message(CommandStart(deep_link=True))
async def start_with_link(message: Message, command):
    code = command.args

    file_id = get_video(code)

    if not file_id:
        await message.answer("❌ ভিডিও পাওয়া যায়নি।")
        return

    await bot.send_video(
        chat_id=message.chat.id,
        video=file_id,
        caption="🎬 আপনার ভিডিও"
    )


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 স্বাগতম!\n\nঅ্যাডমিনের দেওয়া লিংকে Start চাপলে ভিডিও পাবেন।"
    )async def main():
    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
