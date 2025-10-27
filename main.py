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
@app_commands.describe(user="バンするユーザー(IDも含む)", reason="理由")
async def ban(interaction: discord.Interaction, user: str, reason: str = "理由なし"):
    guild = interaction.guild

    if not guild:
        await interaction.response.send_message("❌ このコマンドはサーバー内でのみ使用できます。", ephemeral=True)
        return

    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("🚫 あなたにはBAN権限がありません。", ephemeral=True)
        return

    target = None
    display_name = ""
    try:
        # --- メンション形式の場合 ---
        if user.startswith("<@") and user.endswith(">"):
            user_id = int(user.replace("<@", "").replace(">", "").replace("!", ""))
        else:
            # ID指定
            user_id = int(user)

        # サーバー内メンバーを優先して取得
        target = guild.get_member(user_id)
        if target:
            display_name = str(target)
        else:
            # サーバー外ユーザーの場合、Userオブジェクトを取得
            try:
                target = await bot.fetch_user(user_id)
                display_name = f"{target} (ID: {target.id})"
            except discord.NotFound:
                # 存在しないID
                target = discord.Object(id=user_id)
                setattr(target, "_display_name", f"Unknown User ({user_id})")
                display_name = getattr(target, "_display_name")

        # --- BAN実行 ---
        await guild.ban(target, reason=reason, delete_message_seconds=0)
        await interaction.response.send_message(f"🔨 {display_name} をサーバーからBANしました。\n理由: {reason}")

    except ValueError:
        await interaction.response.send_message("❌ 無効なユーザー指定です。メンションまたは数値IDを指定してください。", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("⚠️ 権限不足でBANできませんでした。", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ エラー: {e}", ephemeral=True)

@bot.tree.command(name="unban", description="ユーザーのBANを解除します（メンションまたはID指定）")
@app_commands.describe(
    user="アンバンするユーザー（ユーザーIDも含む）"
)
async def unban(interaction: discord.Interaction, user: str):
    guild = interaction.guild

    if not guild:
        await interaction.response.send_message("❌ このコマンドはサーバー内でのみ使用できます。", ephemeral=True)
        return

    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("🚫 あなたにはBAN解除権限がありません。", ephemeral=True)
        return

    target_id = None
    display_name = ""
    try:
        # --- メンション形式 ---
        if user.startswith("<@") and user.endswith(">"):
            target_id = int(user.replace("<@", "").replace(">", "").replace("!", ""))
        else:
            # ID指定
            target_id = int(user)

        # バンリストを取得して確認
        bans = await guild.bans()
        ban_entry = discord.utils.find(lambda b: b.user.id == target_id, bans)
        if not ban_entry:
            await interaction.response.send_message(f"❌ ユーザーID `{target_id}` はBANされていません。", ephemeral=True)
            return

        # ユーザー情報を取得（表示用）
        try:
            target_user = await bot.fetch_user(target_id)
            display_name = f"{target_user} (ID: {target_user.id})"
        except discord.NotFound:
            display_name = f"Unknown User ({target_id})"

        # --- アンバン実行 ---
        await guild.unban(discord.Object(id=target_id))
        await interaction.response.send_message(f"🔓 {display_name} のBANを解除しました。")

    except ValueError:
        await interaction.response.send_message("❌ 無効なユーザー指定です。メンションまたは数値IDを指定してください。", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("⚠️ 権限不足でBAN解除できませんでした。", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ エラー: {e}", ephemeral=True)

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