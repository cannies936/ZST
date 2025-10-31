@bot.tree.command(name="serverinfo", description="サーバーの情報を表示します")
async def server_info(interaction: discord.Interaction):

    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message("❌ このコマンドはサーバー内でのみ使用できます", ephemeral=True)
        return

    owner = guild.owner
    created_at = guild.created_at
    member_count = guild.member_count
    
    text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
    voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
    categories = len([c for c in guild.channels if isinstance(c, discord.CategoryChannel)])
    total_channels = len(guild.channels)

    role_count = len(guild.roles) - 1

    humans = len([m for m in guild.members if not m.bot])
    bots = len([m for m in guild.members if m.bot])

    online_members = len([m for m in guild.members if m.status == discord.Status.online])
    idle_members = len([m for m in guild.members if m.status == discord.Status.idle])
    dnd_members = len([m for m in guild.members if m.status == discord.Status.dnd])
    offline_members = len([m for m in guild.members if m.status == discord.Status.offline])

    verification_level = str(guild.verification_level).replace('_', ' ').title()
    content_filter = str(guild.explicit_content_filter).replace('_', ' ').title()

    boost_level = guild.premium_tier
    boost_count = guild.premium_subscription_count or 0

    features = []
    if guild.features:
        feature_names = {
            'VERIFIED': '✅ 認証済み',
            'PARTNERED': '🤝 パートナー',
            'COMMUNITY': '🏘️ コミュニティ',
            'NEWS': '📰 ニュース',
            'DISCOVERABLE': '🔍 発見可能',
            'VANITY_URL': '🔗 カスタムURL',
            'BANNER': '🎨 バナー',
            'ANIMATED_ICON': '✨ アニメーションアイコン',
            'BOOST_LEVEL_1': '🚀 ブーストレベル1',
            'BOOST_LEVEL_2': '🚀 ブーストレベル2',
            'BOOST_LEVEL_3': '🚀 ブーストレベル3'
        }
        features = [feature_names.get(f, f) for f in guild.features[:10]]

    embed = discord.Embed(
        title=f"📊 {guild.name} サーバー情報",
        description=f"サーバーID: `{guild.id}`",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(name="👑 所有者", value=f"{owner}\n(ID: {owner.id})", inline=True)
    embed.add_field(name="📅 作成日", value=f"{created_at.strftime('%Y/%m/%d')}", inline=True)
    embed.add_field(name="🔒 認証レベル", value=verification_level, inline=True)

    embed.add_field(name="👥 メンバー数", value=f"総数: {member_count}\n人間: {humans}\nBOT: {bots}", inline=True)
    embed.add_field(name="📈 オンライン状況", value=f"🟢 {online_members} / 🟡 {idle_members} / 🔴 {dnd_members} / ⚫ {offline_members}", inline=True)
    embed.add_field(name="📺 チャンネル", value=f"総数: {total_channels}\n💬 {text_channels} / 🔊 {voice_channels} / 📁 {categories}", inline=True)

    embed.add_field(name="🎭 ロール数", value=str(role_count), inline=True)

    if boost_level > 0 or boost_count > 0:
        emoji = ["", "🥉", "🥈", "🥇"][boost_level] if boost_level < 4 else "💎"
        embed.add_field(name=f"{emoji} ブースト", value=f"レベル {boost_level}\n{boost_count} ブースト", inline=True)
    else:
        embed.add_field(name="🚀 ブースト", value="未ブースト", inline=True)

    embed.add_field(name="🛡️ コンテンツフィルタ", value=content_filter, inline=True)

    if features:
        embed.add_field(name="⭐ 機能", value="\n".join(features), inline=False)

    embed.set_footer(text=f"情報取得者: {interaction.user}", icon_url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)
