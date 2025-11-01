@bot.tree.command(name="skip", description="次の曲にスキップします")
async def skip(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await interaction.response.send_message("⏭ スキップしました")
    else:
        await interaction.response.send_message("⚠ 再生中の曲がありません")