import os
import discord
from discord.ext import commands
import google.generativeai as genai

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        try:
            content = message.content.replace(f"<@{bot.user.id}>", "").strip()
            if not content:
                content = "Salut !"
            resp = model.generate_content(content)
            await message.channel.send(resp.text)
        except Exception as e:
            await message.channel.send("❌ Erreur API.")
            print(e)

bot.run(DISCORD_TOKEN)
