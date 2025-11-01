@bot.tree.command(name="play", description="YouTubeのURLまたは検索ワードを再生します。")
async def play(interaction: discord.Interaction, query: str):
    await interaction.response.defer()

    voice = interaction.guild.voice_client

    if not voice:
        if interaction.user.voice:
            voice = await interaction.user.voice.channel.connect()
        else:
            await interaction.followup.send("⚠ ボイスチャンネルに参加してから実行してください。")
            return

    queue = get_player(interaction.guild_id)

    # YouTubeリンクでなければ検索する
    if not query.startswith("http"):
        query = f"ytsearch:{query}"

    queue.append(query)

    if not voice.is_playing():
        await play_next(interaction)
        await interaction.followup.send(f"🎶 再生開始: **{query}**")
    else:
        await interaction.followup.send(f"➕ キューに追加: **{query}**")