from pyrogram import Client, filters
from config import *
from database import save_file
from utils import generate_hash

bot = Client(
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.private & (filters.video | filters.document))
async def handle_file(client, message):
    file = message.video or message.document

    _id = save_file(
        file.file_id,
        file.file_name,
        file.file_size,
        file.mime_type
    )

    hash_value = generate_hash(str(_id))
    link = f"{BASE_URL}/watch/{_id}?hash={hash_value}"

    await message.reply_text(f"🎬 Watch Link:\n{link}")

bot.run()
