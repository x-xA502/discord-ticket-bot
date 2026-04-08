import discord
from discord.ext import commands
import json
import os
from datetime import datetime
import nest_asyncio

nest_asyncio.apply()

# إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

# متغيرات عامة
tickets = {}
ticket_count = 0

@bot.event
async def on_ready():
    print(f'✅ البوت جاهز! تم تسجيل الدخول: {bot.user}')
    await bot.tree.sync()

# أمر الاختبار
@bot.command()
async def hello(ctx):
    await ctx.send(f'مرحبا {ctx.author.mention}! 👋')

# Slash Command: /ticket
@bot.tree.command(name="ticket", description="إنشاء تيكت جديد")
async def ticket_command(interaction: discord.Interaction):
    guild = interaction.guild
    
    # احصل على جميع الكاتيجوريات
    categories = [c for c in guild.categories]
    
    if not categories:
        await interaction.response.send_message("❌ لا توجد كاتيجوريات في السيرفر!", ephemeral=True)
        return
    
    # إنشاء Dropdown للاختيار بين الكاتيجوريات
    class CategorySelect(discord.ui.Select):
        def __init__(self, categories):
            options = [discord.SelectOption(label=cat.name, value=str(cat.id)) for cat in categories]
            super().__init__(placeholder="اختر الكاتيجوري الذي تريد فتح التيكت فيه", options=options)
        
        async def callback(self, interaction: discord.Interaction):
            category_id = int(self.values[0])
            category = guild.get_channel(category_id)
            
            if not category:
                await interaction.response.send_message("❌ حدث خطأ في البحث عن الكاتيجوري", ephemeral=True)
                return
            
            # إنشاء قناة التيكت
            global ticket_count
            ticket_count += 1
            ticket_name = f"ticket-{ticket_count}-{interaction.user.name}"
            
            try:
                ticket_channel = await category.create_text_channel(
                    name=ticket_name,
                    topic=f"التيكت الخاص بـ {interaction.user.mention}"
                )
                
                # حفظ بيانات التيكت
                tickets[ticket_channel.id] = {
                    'user': interaction.user.id,
                    'created_at': datetime.now().isoformat(),
                    'category_id': category_id,
                    'messages': []
                }
                
                # رسالة ترحيبية
                embed = discord.Embed(
                    title="🎫 مرحباً بك في التيكت",
                    description=f"شكراً لفتحك تيكت جديد! 🎉\n\nسيتم الرد على استفسارك قريباً.",
                    color=discord.Color.green()
                )
                embed.set_footer(text=f"رقم التيكت: {ticket_count}")
                
                await ticket_channel.send(embed=embed)
                await interaction.response.send_message(f"✅ تم إنشاء التيكت في {ticket_channel.mention}", ephemeral=True)
                
            except Exception as e:
                await interaction.response.send_message(f"❌ حدث خطأ: {str(e)}", ephemeral=True)
    
    view = discord.ui.View()
    view.add_item(CategorySelect(categories))
    
    await interaction.response.send_message("اختر الكاتيجوري:", view=view, ephemeral=True)

# شغل البوت
if __name__ == '__main__':
    bot.run('YOUR_TOKEN_HERE')
