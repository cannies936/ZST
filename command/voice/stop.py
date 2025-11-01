@bot.tree.command(name="stop", description="再生を停止し、キューをクリアします")
async def stop(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    queue = get_player(interaction.guild_id)

    queue.clear()
    if vc:
        vc.stop()
    await interaction.response.send_message("🛑 停止＆キューをクリアしました")