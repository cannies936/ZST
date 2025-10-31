@bot.tree.command(name="autodeleteinvite", description="招待作成時の自動削除をオン/オフします。")
@app_commands.describe(state="true でオン、false でオフにします。")
async def deleteinvite(interaction: discord.Interaction, state: bool):
    global auto_delete_invites  # ← 追加

    guild_id = interaction.guild_id
    auto_delete_invites[guild_id] = state

    if state:
        await interaction.response.send_message("✅ 招待自動削除モードを **ON** にしました。")
    else:
        await interaction.response.send_message("❎ 招待自動削除モードを **OFF** にしました。")


@bot.event
async def on_invite_create(invite: discord.Invite):
    guild_id = invite.guild.id

    if auto_delete_invites.get(guild_id, False):
        try:
            await invite.delete(reason="自動削除モードが有効です。")
            print(f"🔸 招待を自動削除しました: {invite.code}")
        except Exception as e:
            print(f"❌ 招待削除エラー: {e}")