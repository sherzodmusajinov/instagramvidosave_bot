import os
import asyncio
import instaloader
import requests
from aiogram import Bot, Dispatcher, types

TOKEN = "7941424392:AAE0BFodAFJA8eTlG4bcA744jfwM7i-goI0"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

loader = instaloader.Instaloader()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Отправь мне ссылку на Instagram-видео, и я скачаю его для тебя.")


@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text
    if "instagram.com" not in url:
        await message.reply("Отправьте корректную ссылку на Instagram-видео!")
        return

    await message.reply("Получаю видео, подождите...")

    try:
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        video_url = post.video_url

        if not video_url:
            await message.reply("Не удалось найти видео на этой странице.")
            return

        video_path = "instagram_video.mp4"
        response = requests.get(video_url, stream=True)
        with open(video_path, "wb") as video_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    video_file.write(chunk)

        await message.reply("Отправляю видео...")
        with open(video_path, "rb") as video:
            await message.answer_video(video, caption="Вот ваше видео из Instagram.")
        os.remove(video_path)
    except Exception as e:
        await message.reply(f"Ошибка при получении видео: {e}")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
