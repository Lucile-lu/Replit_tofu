import discord
from discord.ext import commands
import os
import random
import time

# ===== 設定機器人權限與前綴 =====
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# ===== 啟動時訊息 =====
@bot.event
async def on_ready():
    print(f"✅ 登入成功 --> {bot.user}")

# ===== 指令：#豆腐 =====
@bot.command()
async def 豆腐(ctx):
    await ctx.send("我是玲玲的豆腐🐶")

# ===== 關鍵詞對應訊息與檔案 =====
KEYWORDS = {
    "情侶": {
        "text": "💡 來自豆腐的小提醒：請專注我們可愛的玲玲喔☺️",
        "file": "hehe.gif"},
    "orm": {
        "text": "💡 來自豆腐的小提醒：請專注我們可愛的玲玲喔☺️",
        "file": "hehe.gif"},
    "好嗑": {
        "text": "💡 來自豆腐的小提醒：請專注我們可愛的玲玲喔☺️",
        "file": "hehe.gif"},
    "愛嗑": {
        "text": "💡 來自豆腐的小提醒：請專注我們可愛的玲玲喔☺️",
        "file": "hehe.gif"},
    "陳奧": {
        "text": "💡 來自豆腐的小提醒：請專注我們可愛的玲玲喔☺️",
        "file": "hehe.gif"},
    "陳美玲": {
        "text": "💡 來自豆腐的小提醒：請專注我們可愛的玲玲喔☺️",
        "file": "hehe.gif"},
    "奧比": {
        "text": "💡 來自豆腐的小提醒：請專注我們可愛的玲玲喔☺️",
        "file": "hehe.gif"},
    "korn": {
        "text": "💡 來自豆腐的小提醒：請專注我們可愛的玲玲喔☺️",
        "file": "hehe.gif"},
    "豆腐": {
        "text": "我是豆腐，雖然媽媽常忘了我🥹，但只要你提到某些詞，我就會跑出來提醒你喔🐶",
        "file": "poor tofu.jpg"
    },
    "豆腐晚安": {
        "text": "💤💤💤",
        "file": None
    },
    "晚安豆腐": {
        "text": "💤💤💤",
        "file": None
    }
}

# ===== 早安 GIF 檔案路徑 =====
GIF_FOLDER = "gifs"
RATE_LIMIT_SECONDS = 30
_last_sent_per_channel = {}

# ===== 當有人發訊息時觸發 =====
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("#"):
        await bot.process_commands(message)
        return

    msg_lower = message.content.lower()

    # ===== 觸發「早安」關鍵詞 =====
    if "早安" in msg_lower:
        channel_id = message.channel.id
        now = time.time()
        last = _last_sent_per_channel.get(channel_id, 0)

        if now - last >= RATE_LIMIT_SECONDS:
            # 隨機選一張 GIF 檔案
            gif_files = [f for f in os.listdir(GIF_FOLDER) if f.endswith((".gif", ".mp4"))]
            if not gif_files:
                await message.channel.send("❌ 找不到任何 GIF，請確認 gifs 資料夾有檔案。")
                return

            chosen_gif = random.choice(gif_files)
            file_path = os.path.join(GIF_FOLDER, chosen_gif)

            embed = discord.Embed(
                title="☀️ 早安～",
                description=f"{message.author.mention} 祝你有個開心的一天！",
                color=0xFFD580
            )
            embed.set_footer(text="由豆腐🐶送上")

            await message.channel.send(embed=embed, file=discord.File(file_path))
            _last_sent_per_channel[channel_id] = now
        else:
            return

    # ===== 關鍵詞觸發文字或檔案 =====
    for key, info in KEYWORDS.items():
        if key in msg_lower:
            text = info.get("text")
            file_path = info.get("file")

            if file_path:
                if os.path.exists(file_path):
                    await message.channel.send(text, file=discord.File(file_path))
                else:
                    await message.channel.send(f"{text}\n❌ 找不到檔案: {file_path}")
            else:
                await message.channel.send(text)
            return

    await bot.process_commands(message)

# ===== 啟動機器人 =====
TOKEN = os.getenv("DISCORD_TOKEN_TOFU")

if not TOKEN:
    print("❌ 找不到環境變數 DISCORD_TOKEN_TOFU，請在 Secrets 設定 Token")
else:
    bot.run(TOKEN)
