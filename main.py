import discord
import random
import re
import os
import asyncio
import glob
from discord.ext import commands
from typing import Optional
from collections import defaultdict, deque
import time

token = "YOUR_BOT_TOKEN"

# Discordボット設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # サーバー参加・退出イベントに必要
intents.members = True  # メンバー情報取得に必要
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
     if bot.user:
        print(f'{bot.user} としてログインしました！')
        print(f'Bot ID: {bot.user.id}')
        print('ボットが準備完了です！')
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(''))
        await bot.tree.sync()


bot.run(token)