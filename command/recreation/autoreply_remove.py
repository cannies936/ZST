@bot.tree.command(name="autoreply_remove", description="自動返信を削除します。")
@app_commands.describe(keyword="削除するワード")
async def autoreply_remove(interaction: discord.Interaction, keyword: str):
    keyword = keyword.lower()
    
    if keyword in auto_reply_dict:
        del auto_reply_dict[keyword]
        await interaction.response.send_message(f"🗑 自動返信を削除しました：**{keyword}**")
    else:
        await interaction.response.send_message("❌ そのワードは登録されていません。")
