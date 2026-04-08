import discord
from discord.ext import commands
import asyncio
import json
import os
from datetime import datetime

# إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# متغيرات عامة
ticket_count = 0
tickets = {}

@bot.event
async def on_ready():
    print(f'✅ البوت جاهز! تم تسجيل الدخول: {bot.user}')
    await bot.tree.sync()

# أمر الاختبار
@bot.command()
async def hello(ctx):
    await ctx.send(f'مرحبا {ctx.author.mention}! 👋')

# شغل البوت
await bot.start('YOUR_TOKEN_HERE')
