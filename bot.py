import discord
from discord import app_commands
from discord.ext import commands
import asyncio

# Botun yetkilerini (Intents) ayarlıyoruz
intents = discord.Intents.default()
intents.members = True  # Üye listesine erişim için şart
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Slash komutlarını senkronize eder
        await self.tree.sync()
        print(f"Komutlar senkronize edildi.")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Bot {bot.user} olarak giriş yaptı!')

@bot.tree.command(name="duyuru", description="Sunucudaki herkese özel mesaj atar.")
@app_commands.describe(mesaj="Gönderilecek mesajı yazın")
@commands.has_permissions(administrator=True) # Sadece yöneticiler kullanabilsin
async def duyuru(interaction: discord.Interaction, mesaj: str):
    await interaction.response.send_message("Duyuru işlemi başlatıldı...", ephemeral=True)
    
    basarili = 0
    hatali = 0
    
    for member in interaction.guild.members:
        if member.bot: # Botları atla
            continue
            
        try:
            await member.send(mesaj)
            basarili += 1
            await asyncio.sleep(0.5) # Discord sınırlarına takılmamak için kısa bekleme
        except discord.Forbidden:
            # Kullanıcı DM'lerini kapatmışsa hata verir
            hatali += 1
        except Exception as e:
            hatali += 1

    await interaction.followup.send(f"İşlem tamamlandı!\n✅ Başarılı: {basarili}\n❌ Başarısız (DM Kapalı vb.): {hatali}")

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
