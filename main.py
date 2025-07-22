import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from keep_alive import keep_alive

# Charger les variables d’environnement depuis le fichier .env
load_dotenv()

# Lancer le mini-serveur Flask pour garder Replit en ligne
keep_alive()

# Configuration des intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1396914289511764038  # Remplace par l’ID de ton serveur

class RulesButton(discord.ui.View):
    def __init__(self, role_id):
        super().__init__(timeout=None)
        self.role_id = role_id

    @discord.ui.button(label="✅", style=discord.ButtonStyle.success, custom_id="rules_accept")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.role_id)
        if role in interaction.user.roles:
            await interaction.response.send_message("Tu as déjà le rôle !", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Rôle 'Membre' attribué avec succès !", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"✅ Connecté en tant que {bot.user}")

@bot.tree.command(name="rules", description="Envoie les règles du serveur", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def rules_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Rules",
        description="By checking this box you accept the terms of use of this discord server",
        color=0x00ff00
    )
    embed.set_thumbnail(url="https://p16-pu-sign-no.tiktokcdn-eu.com/tos-no1a-avt-0068c001-no/f41580b277df1be78451a27e2320cc42~tplv-tiktokx-cropcenter:1080:1080.jpeg?dr=10399&refresh_token=dfc9f9f9&x-expires=1753344000&x-signature=Gtdj9T7LY7Py4g0hQO%2FKhYSUN3M%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=no1a")

    role = discord.utils.get(interaction.guild.roles, name="Membre")
    if not role:
        await interaction.response.send_message("Le rôle 'Membre' n'existe pas.", ephemeral=True)
        return

    view = RulesButton(role.id)
    await interaction.response.send_message(embed=embed, view=view)

@rules_command.error
async def rules_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ Seuls les administrateurs peuvent utiliser cette commande.", ephemeral=True)

# Récupération du token depuis .env
token = os.getenv("DISCORD_TOKEN")

if token is None:
    print("❌ Token non trouvé. Vérifie ton fichier .env.")
else:
    bot.run(token)
