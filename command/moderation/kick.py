@bot.tree.command(name="kick", description="ユーザーをサーバーからキックします")
@app_commands.describe(user="キックするユーザー", reason="理由")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "理由はありません"):
    
   # 理由の長さ制限（Discord API制限対応）
    audit_reason = f"実行者: {interaction.user} | 理由: {reason}"     
    
    await interaction.guild.kick(user, reason=audit_reason)
    
    embed = discord.Embed(
        title=f"Kick result",
        description=f"{user.display_name} をサーバーからkickしました。\n理由: {reason} \n実行者: {interaction.user}",
        color=discord.Color.yellow(),
        timestamp=discord.utils.utcnow()
    )
    
    await interaction.response.send_message(embed=embed)
