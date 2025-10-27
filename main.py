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
intents.invites = True
intents.members = True  # メンバー情報取得に必要
bot = commands.Bot(command_prefix='!', intents=intents)

# コマンドツリーを作成
tree = bot.tree

# 送信したいURLリスト
url_list = [
    "https://cdn.discordapp.com/attachments/1396664286889250906/1429641976604655636/sprite_bottle_2.jpg?ex=68feca58&is=68fd78d8&hm=b5776df38faa4164fb72099d3a2d661b477cb9421a25d4183dd1a2fbeec415e1&",
    "https://cdn.discordapp.com/attachments/1396664286889250906/1429641858887450675/sprite_can_1.png?ex=68feca3c&is=68fd78bc&hm=1d1906a7134fa858bc79ebc1029e06a00c623c74c0a20e664c5c9b37d47643a6&",
    "https://cdn.discordapp.com/attachments/1396664286889250906/1429641659896959162/sprite_bottle_1.png?ex=68feca0d&is=68fd788d&hm=ab01677545fe0c04e9d92b9cc4c433f5a9957856f51b590eadfbea809ffdec5f&",
    "https://cdn.discordapp.com/attachments/1396664286889250906/1429641247374708746/sprite_image_3.jpg?ex=68fec9aa&is=68fd782a&hm=c6d4765846a2fff593988de3ed61847a62ac133ead652f77946ed358baf605d5&"
    ]

@bot.event
async def on_ready():
await bot.tree.sync()     
     if bot.user:
        print(f'{bot.user} としてログインしました！')
        print(f'Bot ID: {bot.user.id}')
        print('ボットが準備完了です！')
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('https://github.com/cannies936/ZST'))
        await bot.tree.sync()

@bot.tree.command(name="ping", description="Botの応答時間を確認します")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

@bot.tree.command(name="supurito", description="ランダムなスプライト画像を表示します")
async def supurito(interaction: discord.Interaction):
    random_url = random.choice(url_list)
    await interaction.response.send_message({random_url})

@bot.tree.command(name="ban", description="ユーザーをサーバーからバンします")
@app_commands.describe(user="バンするユーザー", reason="理由")

@bot.tree.command(name="kick", description="ユーザーをサーバーからキックします")
@app_commands.describe(user="バンするユーザー", reason="理由")

@bot.tree.command(name="timeout", description="ユーザーをタイムアウトします")
@app_commands.describe(user="タイムアウトをするユーザー",time=タイムアウトをする時間を指定します, reason="理由")

@bot.tree.command(name="deleteinvite", description="招待作成時の自動削除をオン/オフします。")
@app_commands.describe(state="true でオン、false でオフにします。")
async def deleteinvite(interaction: discord.Interaction, state: bool):
    guild_id = interaction.guild_id
    auto_delete_invites[guild_id] = state
    if state:
        await interaction.response.send_message("✅ 招待自動削除モードを **ON** にしました。")
    else:
        await interaction.response.send_message("❎ 招待自動削除モードを **OFF** にしました。")

# --- 招待作成イベント ---
@bot.event
async def on_invite_create(invite: discord.Invite):
    guild_id = invite.guild.id
    if auto_delete_invites.get(guild_id, False):
        try:
            await invite.delete(reason="自動削除モードが有効です。")
            print(f"🔸 招待を自動削除しました: {invite.code}")
        except discord.Forbidden:
            print("⚠️ 権限不足で招待を削除できませんでした。")
        except Exception as e:
            print(f"❌ 招待削除中にエラー発生: {e}")

bot.run(token)