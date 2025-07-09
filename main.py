from pyrogram import Client, filters
import openai
import asyncio
import random
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

bot = Client("gojorubot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def gpt_reply(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Gojoru – a funny, intelligent, stylish AI. Talk casually and friendly."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response['choices'][0]['message']['content']

@bot.on_message(filters.text & ~filters.edited)
async def reply(client, message):
    if message.from_user.is_bot:
        return
    try:
        user_msg = message.text
        await message.chat.send_action("typing")
        await asyncio.sleep(random.uniform(0.5, 1.2))
        response = await gpt_reply(user_msg)
        await message.reply(response)
    except Exception as e:
        print(e)
        await message.reply("Sorry... kuch error aa gaya 💀")

bot.run()
