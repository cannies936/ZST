@bot.tree.command(name="about", description="このBotの情報を表示します")
async def about(interaction: discord.Interaction):
    embed = discord.Embed(
        title="ℹ️ ZSTの情報",
        description="BotID: 1431588391467749467",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name="Botname", value="ZST#9315", inline=True)
    embed.add_field(name="作者", value="cannies236._50937", inline=True)
    embed.add_field(name="作者ID", value="1362035197255749884", inline=True)
    embed.add_field(name="ソースコード", value="https://github.com/cannies936/ZST", inline=True)

    await interaction.response.send_message(embed=embed)
