@bot.tree.command(name="loop", description="再生中の曲をループ再生します。")
@app_commands.describe(state="on または off")
async def loop(interaction: discord.Interaction, state: str):
    guild_id = interaction.guild_id

    if state.lower() == "on":
        loop_enabled[guild_id] = True
        await interaction.response.send_message("🔁 ループ再生を **ON** にしました。")
    elif state.lower() == "off":
        loop_enabled[guild_id] = False
        await interaction.response.send_message("➡ ループ再生を **OFF** にしました。")
    else:
        await interaction.response.send_message("⚠ 使い方: `/loop on` または `/loop off`")