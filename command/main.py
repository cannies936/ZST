import discord
import random
import re
import os
import asyncio
import glob
from discord.ext import commands
from discord import app_commands
from typing import Optional
from collections import defaultdict, deque
import time

# --- インテント設定（必須） ---
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容の取得を有効にする




# Discordボット設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # サーバー参加・退出イベントに必要
intents.members = True  # メンバー情報取得に必要
intents.guilds = True  # サーバー参加・退出イベントに必要
intents.invites = True
intents.members = True  # メンバー情報取得に必要
bot = commands.Bot(command_prefix='/', intents=intents)

# コマンドツリーを作成
tree = bot.tree

@bot.event 
async def on_ready():
    await bot.tree.sync()    
    if bot.user:
    　 print(f'{bot.user} としてログインしました！')
      print(f'Bot ID: {bot.user.id}')
      print('ボットが準備完了です！')  

bot.run(token)             

