@bot.tree.command(name="dice", description="サイコロを振ります")
@app_commands.describe(sides="サイコロの面の数（例: 6 → 6面サイコロ）")
async def dice(interaction: discord.Interaction, sides: int = 6):
    if sides < 2:
        await interaction.response.send_message("⚠️ 2以上の数を入力してください。", ephemeral=True)
        return
    
    result = random.randint(1, sides)
    await interaction.response.send_message(f"🎲 **{sides}面サイコロの結果:{result}**")