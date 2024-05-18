# pip install -U aiogram

"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


API_TOKEN = 'token from https://t.me/BotFather'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(regexp='(^push?$|puss)')
async def cats(message: types.Message):
    import time
    from glob import glob
    path = 'photos/*.jpg'
    images = glob(path)
    i = 1
    for image in images:
        if (i:= i + 1) % 2 == 0:
            time.sleep(1)
            print(i)
        with open(image, 'rb') as photo:
            await bot.send_photo(message.chat.id, photo), #caption='Cats is here 😺', reply_to_message_id=message.message_id)


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photos = message.photo  
    file_id = photos[-1].file_id 
    '''
    Когда пользователь присылает боту изображение ( активным режимом сжатия),
    Telegram присылает не один объект,а целый массив с разными размерами одного
    и того же изображения, отсортированными по возрастанию.
    В общем случае нас будет интересовать изображение наибольшего
    размера, стоящее последним (индекс «минус один»).
    '''
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    # Здесь вы можете сохранить фотографию в нужное место, указав путь,
    # например, используя модуль os.

    import os
    save_path = os.path.join('telephotos/', f'{file_id}.jpg')
    await bot.download_file(file_path, save_path)
    # Теперь фотография сохранена в указанном пути.


# @dp.message_handler(content_types=["text", "photo", "video"])
# async def process_start_command(message: types.Message):
#     await bot.forward_message(message.from_user.id, message.from_user.id, message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)