import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# VoidX Studios - Muazzam Elektrik Animasyonlu Ana Sayfa
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoidX Studios | Render Proxy</title>
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
                <span>Render Cloud Aktif</span>
            </div>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-6 py-12 flex-grow w-full text-center">
        <h1 class="text-4xl md:text-5xl font-black tracking-tight mb-4 bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
            VoidX Render Proxy Köprüsü
        </h1>
        <p class="text-slate-400 text-lg max-w-2xl mx-auto mb-8">
            Render altyapısıyla Cloudflare engeline takılmayan kesintisiz API köprüsü.
        </p>
        <div class="bg-slate-900/40 border border-slate-800 rounded-3xl p-8 backdrop-blur-md inline-block">
            <button onclick="triggerSparks(event)" class="electric-btn relative bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold px-8 py-4 rounded-2xl shadow-xl shadow-blue-500/20 cursor-pointer">
                <i class="fa-solid fa-bolt mr-2"></i> Sistemi Ateşle
            </button>
        </div>
    </main>
    <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <p>VoidX Studios © 2026 — Render Cloud Architecture</p>
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
    data = request.json or {}
    token = data.get("token")
    action = data.get("action")
    channel_id = data.get("channel_id")
    content = data.get("content")

    if not token:
        return jsonify({"error": "Token alanı boş olamaz."}), 400

    auth_header = token if token.startswith("Bot ") or token.startswith("Bearer ") else f"Bot {token}"
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        if action == "overview":
            overview_result = []
            guilds_res = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
            if guilds_res.status_code != 200:
                return jsonify({"error": "Sunucular alınamadı.", "details": guilds_res.text}), 400
            
            guilds = guilds_res.json()
            if isinstance(guilds, list):
                for g in guilds:
                    g_id = g.get("id")
                    g_name = g.get("name")
                    if not g_id:
                        continue
                    ch_res = requests.get(f"https://discord.com/api/v10/guilds/{g_id}/channels", headers=headers)
                    if ch_res.status_code == 200:
                        try:
                            channels = ch_res.json()
                            if isinstance(channels, list):
                                text_channels = [{"id": c.get("id"), "name": c.get("name")} for c in channels if c.get("type") == 0 and c.get("id")]
                                if text_channels:
                                    overview_result.append({"server_name": g_name, "channels": text_channels})
                        except:
                            pass

            dm_res = requests.get("https://discord.com/api/v10/users/@me/channels", headers=headers)
            if dm_res.status_code == 200:
                dm_channels = dm_res.json()
                if isinstance(dm_channels, list) and dm_channels:
                    dm_list = []
                    for dm in dm_channels:
                        recipients = dm.get("recipients", [])
                        dm_name = recipients[0].get("username", "Özel Sohbet") if recipients else f"DM ({dm.get('id')})"
                        dm_list.append({"id": dm.get("id"), "name": dm_name})
                    overview_result.append({"server_name": "Özel Mesajlar (DM)", "channels": dm_list})

            if not overview_result:
                return jsonify({"error": "Erişilebilen kanal bulunamadı."}), 400

            return jsonify(overview_result)

        elif action == "fetch":
            if not channel_id:
                return jsonify({"error": "Kanal ID gerekli."}), 400
            msg_res = requests.get(f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=20", headers=headers)
            if msg_res.status_code != 200:
                return jsonify({"error": "Mesajlar çekilemedi.", "details": msg_res.text}), 400
            return jsonify(msg_res.json())

        elif action == "send":
            if not channel_id or not content:
                return jsonify({"error": "Kanal ID ve mesaj içeriği gerekli."}), 400
            res = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers=headers, json={"content": content})
            return jsonify(res.json()), res.status_code

        return jsonify({"error": "Geçersiz action."}), 400

    except Exception as err:
        return jsonify({"error": "Sunucu içi hata", "details": str(err)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
