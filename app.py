import os
import threading
import asyncio
from flask import Flask, render_template_string, request, jsonify
import discord
from discord.ext import commands

app = Flask(__name__)

# Discord Bot Gateway (WebSocket) Yapılandırması
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Android uygulama için sunucu içi hızlı önbellek
cache_data = {
    "ready": False,
    "guilds": []
}

@bot.event
async def on_ready():
    print(f"[VoidX Bot] Gateway Bağlantısı Başarılı: {bot.user}")
    cache_data["ready"] = True
    update_guilds_cache()

def update_guilds_cache():
    guilds_list = []
    for guild in bot.guilds:
        channels = [{"id": str(c.id), "name": c.name} for c in guild.text_channels]
        guilds_list.append({
            "server_name": guild.name,
            "channels": channels
        })
    cache_data["guilds"] = guilds_list

# Botu arka planda sürekli aktif tutacak thread
def run_discord_bot():
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        try:
            bot.run(token)
        except Exception as e:
            print(f"Bot başlatılamadı: {e}")

# Arka plan thread'ini başlatıyoruz
threading.Thread(target=run_discord_bot, daemon=True).start()

# VoidX Studios - Elektrik Animasyonlu Ana Sayfa
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoidX Studios | Render Bot Gateway</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .electric-btn { position: relative; overflow: hidden; transition: all 0.3s ease; }
        .electric-btn:active { transform: scale(0.95); }
        .spark { position: absolute; background: cyan; pointer-events: none; opacity: 0; border-radius: 50%; box-shadow: 0 0 10px cyan, 0 0 20px blue; }
        @keyframes sparkAnim {
            0% { transform: translate(var(--startX), var(--startY)) scale(0.5); opacity: 1; }
            100% { transform: translate(0, 0) scale(1.5); opacity: 0; }
        }
        .spark-active { animation: sparkAnim 0.4s ease-out forwards; }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between font-sans selection:bg-blue-500 selection:text-white">
    <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400 shadow-lg shadow-blue-500/20">
                    <i class="fa-solid fa-bolt-lightning text-lg"></i>
                </div>
                <span class="font-bold text-lg tracking-wide bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">VoidX Studios</span>
            </div>
            <div class="flex items-center space-x-2 text-xs bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-3 py-1.5 rounded-full">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>Render Bot Gateway Aktif</span>
            </div>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-6 py-12 flex-grow w-full text-center">
        <h1 class="text-4xl md:text-5xl font-black tracking-tight mb-4 bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
            VoidX Render Bot Bridge
        </h1>
        <p class="text-slate-400 text-lg max-w-2xl mx-auto mb-8">
            Arka planda 7/24 çalışan Discord Bot altyapısı ile engelsiz ve hatasız köprü.
        </p>
        <div class="bg-slate-900/40 border border-slate-800 rounded-3xl p-8 backdrop-blur-md inline-block">
            <button onclick="triggerSparks(event)" class="electric-btn relative bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold px-8 py-4 rounded-2xl shadow-xl shadow-blue-500/20 cursor-pointer">
                <i class="fa-solid fa-bolt mr-2"></i> Gateway Durumunu Test Et
            </button>
        </div>
    </main>
    <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <p>VoidX Studios © 2026 — Gateway Bot Architecture</p>
    </footer>
    <script>
        function triggerSparks(e) {
            const btn = e.currentTarget;
            for (let i = 0; i < 12; i++) {
                const spark = document.createElement('div');
                spark.classList.add('spark');
                const angle = Math.random() * Math.PI * 2;
                const distance = 80 + Math.random() * 60;
                spark.style.setProperty('--startX', (Math.cos(angle) * distance) + 'px');
                spark.style.setProperty('--startY', (Math.sin(angle) * distance) + 'px');
                spark.style.width = '6px'; spark.style.height = '6px';
                btn.appendChild(spark);
                setTimeout(() => spark.classList.add('spark-active'), 10);
                setTimeout(() => spark.remove(), 400);
            }
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/discord", methods=["POST"])
def discord_proxy():
    if not cache_data["ready"]:
        return jsonify({"error": "Bot henüz Discord Gateway'e bağlanıyor, lütfen 5 saniye sonra tekrar deneyin."}), 503

    data = request.json or {}
    action = data.get("action")
    channel_id = data.get("channel_id")
    content = data.get("content")

    if action == "overview":
        update_guilds_cache()
        return jsonify(cache_data["guilds"])

    elif action == "fetch":
        if not channel_id:
            return jsonify({"error": "Kanal ID gerekli."}), 400
        try:
            ch_id_int = int(channel_id)
        except ValueError:
            return jsonify({"error": "Geçersiz Kanal ID formatı."}), 400

        future = asyncio.run_coroutine_threadsafe(fetch_messages_async(ch_id_int), bot.loop)
        try:
            messages = future.result(timeout=6)
            return jsonify(messages)
        except Exception as e:
            return jsonify({"error": "Mesajlar alınamadı", "details": str(e)}), 400

    elif action == "send":
        if not channel_id or not content:
            return jsonify({"error": "Kanal ID ve mesaj içeriği gerekli."}), 400
        try:
            ch_id_int = int(channel_id)
        except ValueError:
            return jsonify({"error": "Geçersiz Kanal ID formatı."}), 400

        future = asyncio.run_coroutine_threadsafe(send_message_async(ch_id_int, content), bot.loop)
        try:
            future.result(timeout=6)
            return jsonify({"status": "success", "message": "Mesaj başarıyla gönderildi."})
        except Exception as e:
            return jsonify({"error": "Mesaj gönderilemedi", "details": str(e)}), 400

    return jsonify({"error": "Geçersiz action."}), 400

async def fetch_messages_async(channel_id):
    channel = bot.get_channel(channel_id)
    if not channel:
        channel = await bot.fetch_channel(channel_id)
    
    messages = []
    async for msg in channel.history(limit=20):
        messages.append({
            "author": {"username": msg.author.name},
            "content": msg.content
        })
    return messages

async def send_message_async(channel_id, content):
    channel = bot.get_channel(channel_id)
    if not channel:
        channel = await bot.fetch_channel(channel_id)
    await channel.send(content)
    return True

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
