auto_reply_dict = {}

@bot.tree.command(name="autoreply_add", description="特定のワードに自動返信を追加します。")
@app_commands.describe(keyword="反応させる単語", reply="返信する内容")
async def autoreply_add(interaction: discord.Interaction, keyword: str, reply: str):
    auto_reply_dict[keyword.lower()] = reply
    await interaction.response.send_message(f"✅ 自動返信を追加しました！\n**{keyword}** → **{reply}**")