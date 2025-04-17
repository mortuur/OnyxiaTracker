import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import json
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

DATA_FILE = 'onyxia_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.command(name='onyxia')
async def onyxia(ctx, action=None):
    data = load_data()
    if action == "kill":
        now = datetime.utcnow()
        data['last_kill'] = now.isoformat()
        save_data(data)
        await ctx.send(f"🗡️ Onyxia kill geregistreerd op {now.strftime('%Y-%m-%d %H:%M UTC')}. Reset over 5 dagen.")
    else:
        if 'last_kill' not in data:
            await ctx.send("Er is nog geen Onyxia kill geregistreerd.")
        else:
            last_kill = datetime.fromisoformat(data['last_kill'])
            next_reset = last_kill + timedelta(days=5)
            remaining = next_reset - datetime.utcnow()
            if remaining.total_seconds() <= 0:
                await ctx.send("🟢 Onyxia is **nu beschikbaar**!")
            else:
                days, seconds = divmod(int(remaining.total_seconds()), 86400)
                hours, seconds = divmod(seconds, 3600)
                minutes = seconds // 60
                await ctx.send(f"⏳ Volgende Onyxia reset over {days}d {hours}u {minutes}m ({next_reset.strftime('%Y-%m-%d %H:%M UTC')})")

# Vervang dit met je eigen bot token
bot.run("YOUR_DISCORD_BOT_TOKEN")
