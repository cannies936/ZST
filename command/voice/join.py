@bot.tree.command(name="join", description="ボイスチャットに参加します 🔊")
async def join(interaction: discord.Interaction):
    # VCに入ってるか確認
    if not interaction.user.voice:
        return await interaction.response.send_message("❌ 先にボイスチャットに参加してください。")

    channel = interaction.user.voice.channel

    # すでに接続している場合は移動
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.move_to(channel)
        return await interaction.response.send_message(f"🔊 **{channel}** に移動しました。")

    # まだ接続していない場合は接続
    await channel.connect(cls=wavelink.Player)
    await interaction.response.send_message(f"✅ ボイスチャット **{channel}** に参加しました。")