@bot.tree.command(name="resume", description="一時停止中の曲を再開します")
async def resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await interaction.response.send_message("▶ 再開しました")
    else:
        await interaction.response.send_message("⚠ 一時停止中の曲がありません")