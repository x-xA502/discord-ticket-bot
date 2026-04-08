import discord
from discord.ext import commands
import json
import os
from datetime import datetime

# إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

ticket_count = 0
tickets = {}

@bot.event
async def on_ready():
    print(f'✅ البوت جاهز! تم تسجيل الدخول: {bot.user}')
    await bot.tree.sync()

@bot.command()
async def hello(ctx):
    await ctx.send(f'مرحبا {ctx.author.mention}! 👋')

# هذا الجزء للعمل مع Google Colab
if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    bot.run('YOUR_TOKEN_HERE')
