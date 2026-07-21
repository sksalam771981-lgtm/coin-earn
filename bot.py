import asyncio
import random
import string

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, ADMIN_ID
from database import save_video, get_video

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


def generate_code():
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))
    @dp.message(F.video)
async def upload_video(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    code = generate_code()
    file_id = message.video.file_id

    save_video(code, file_id)

    me = await bot.get_me()

    await message.answer(
        f"✅ ভিডিও সংরক্ষণ হয়েছে\n\n"
        f"https://t.me/{me.username}?start={code}"
    )
    @dp.message(CommandStart())
async def start(message: Message):
    text = message.text.split()

    if len(text) == 2:
        code = text[1]
        file_id = get_video(code)

        if file_id:
            await message.answer_video(file_id, caption="🎬 আপনার ভিডিও")
        else:
            await message.answer("❌ ভিডিও পাওয়া যায়নি।")
    else:
        await message.answer("👋 স্বাগতম। ভিডিও লিংকে ক্লিক করে Start চাপুন।")
        async def main():
    print("Bot Started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
