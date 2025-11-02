@bot.tree.command(name="timeout", description="指定したユーザーを一定時間タイムアウトさせます")
@app_commands.describe(
    user="タイムアウトするユーザー",
    seconds="タイムアウト時間（分）",
    reason="タイムアウトの理由（任意）"
)
async def timeout(interaction: discord.Interaction, user: discord.Member, seconds: int, reason: str = "理由なし"):
    # 権限チェック
    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ あなたにはユーザーをタイムアウトする権限がありません", ephemeral=True)

    if not interaction.guild.me.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ Bot にタイムアウト権限がありません", ephemeral=True)

    # 自分自身をタイムアウトしようとしているか
    if user.id == interaction.user.id:
        return await interaction.response.send_message("❌ 自分自身をタイムアウトすることはできません。", ephemeral=True)

    # Botをタイムアウトしようとしているか
    if user.id == bot.user.id:
        return await interaction.response.send_message("❌ Bot をタイムアウトすることはできません", ephemeral=True)

    # 権限階層チェック
    if user.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
        return await interaction.response.send_message("❌ あなたより上位または同等のロールを持つユーザーはタイムアウトできません", ephemeral=True)

    # タイムアウト開始
    try:
        await user.timeout(timedelta(seconds=seconds), reason=reason)

        embed = discord.Embed(
            title="⏳ タイムアウト実行",
            description=f"{user.mention} を **{minutes} 秒** タイムアウトしました。",
            color=discord.Color.orange()
        )
        embed.add_field(name="理由", value=reason, inline=False)
        embed.add_field(name="実行者", value=interaction.user.mention, inline=True)

        await interaction.response.send_message(embed=embed)

    except discord.Forbidden:
        await interaction.response.send_message("❌ 権限不足でタイムアウトできませんでした", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ エラーが発生しました: `{e}`", ephemeral=True)
