@bot.tree.command(name="userinfo", description="ユーザー情報を表示します。")
@app_commands.describe(user="情報を確認したいユーザー（未指定なら自分）")
async def userinfo(interaction: discord.Interaction, user: discord.User | None = None):
    # ユーザーが指定されていない場合はコマンド実行者
    user = user or interaction.user

    embed = discord.Embed(
        title=f"👤 ユーザー情報: {user}",
        color=discord.Color.blue()
    )

    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

    embed.add_field(name="ユーザー名", value=f"`{user}`", inline=False)
    embed.add_field(name="ユーザーID", value=f"`{user.id}`", inline=False)

    # guildに存在する場合はサーバー情報も付ける
    if isinstance(user, discord.Member):
        embed.add_field(name="ニックネーム", value=f"`{user.nick}`" if user.nick else "なし", inline=False)
        embed.add_field(
            name="参加日時",
            value=f"<t:{int(user.joined_at.timestamp())}:F>",
            inline=False
        )
        embed.add_field(name="ロール", value=", ".join([role.mention for role in user.roles if role.name != "@everyone"]), inline=False)

    embed.add_field(
        name="アカウント作成日",
        value=f"<t:{int(user.created_at.timestamp())}:F>",
        inline=False
    )

    await interaction.response.send_message(embed=embed)