@bot.tree.command(name="ban", description="ユーザーをサーバーからバンします")
@app_commands.describe(user="バンするユーザー(IDも含む)", reason="理由")
async def ban(interaction: discord.Interaction, user: discord.User, reason: str = "理由はありません"):

 # 理由の長さ制限（Discord API制限対応）
    audit_reason = f"実行者: {interaction.user} | 理由: {reason}"        
    
    await interaction.guild.ban(user, reason=audit_reason)
    
    embed = discord.Embed(
        title=f"Ban result",
        description=f"{user.display_name} をサーバーからバしました。\n理由: {reason} \n実行者: {interaction.user}",
        color=discord.Color.red(),
        timestamp=discord.utils.utcnow()
    )
    
    await interaction.response.send_message(embed=embed)
