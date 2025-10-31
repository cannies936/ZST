# サーバーごとのロックダウン状態保存
lockdown_mode = {}  # { guild_id: "ban" | "kick" | "none" }

@bot.tree.command(name="lockdown", description="サーバー参加者に対して自動で ban / kick / none の処理を行います。")
@app_commands.describe(mode="ban / kick / none のいずれかを選択")
async def lockdown(interaction: discord.Interaction, mode: str):

    mode = mode.lower()

    if mode not in ["ban", "kick", "none"]:
        await interaction.response.send_message("❌ モードは `ban` `kick` `none` のいずれかを指定してください。", ephemeral=True)
        return

    # 状態を保存
    lockdown_mode[interaction.guild_id] = mode

    txt = {
        "ban": "🚫 ロックダウンモード：**BAN**（新規参加者を即BAN）",
        "kick": "⚠️ ロックダウンモード：**KICK**（新規参加者を即Kick）",
        "none": "✅ ロックダウン解除しました（新規参加者は通常通り入れます）"
    }

    await interaction.response.send_message(txt[mode])


# --- 新規メンバー参加時イベント ---
@bot.event
async def on_member_join(member: discord.Member):
    mode = lockdown_mode.get(member.guild.id, "none")

    try:
        if mode == "ban":
            await member.ban(reason="Lockdownモード: 新規参加者を自動BAN")
            print(f"🔨 自動BAN: {member} ({member.id})")

        elif mode == "kick":
            await member.kick(reason="Lockdownモード: 新規参加者を自動Kick")
            print(f"👢 自動Kick: {member} ({member.id})")

        # mode が none の時は何もしない

    except discord.Forbidden:
        print("⚠️ 権限不足でBAN/KICKできませんでした")
    except Exception as e:
        print(f"❌ エラー: {e}")