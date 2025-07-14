from keep_alive import keep_alive
import discord
from discord.ext import commands
import pytesseract
from PIL import Image
import requests
from io import BytesIO
import os

TOKEN = os.environ['DISCORD_TOKEN']
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Conectado como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                response = requests.get(attachment.url)
                img = Image.open(BytesIO(response.content))
                text = pytesseract.image_to_string(img)
                await message.channel.send(f"📝 Texto detectado:\n{text.strip()}")

    await bot.process_commands(message)

keep_alive()
bot.run(TOKEN)
