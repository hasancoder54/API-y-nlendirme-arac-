import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# VoidX Studios - Muazzam Elektrik Animasyonlu ve Şık Ana Sayfa
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoidX Studios | Discord Proxy & Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @keyframes electricPulse {
            0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
            70% { box-shadow: 0 0 0 20px rgba(59, 130, 246, 0); }
            100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
        }
        
        .electric-btn {
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .electric-btn:active {
            transform: scale(0.95);
        }

        .spark {
            position: absolute;
            background: cyan;
            pointer-events: none;
            opacity: 0;
            border-radius: 50%;
            box-shadow: 0 0 10px cyan, 0 0 20px blue;
        }

        @keyframes sparkAnim {
            0% {
                transform: translate(var(--startX), var(--startY)) scale(0.5);
                opacity: 1;
            }
            100% {
                transform: translate(0, 0) scale(1.5);
                opacity: 0;
            }
        }

        .spark-active {
            animation: sparkAnim 0.4s ease-out forwards;
        }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between font-sans selection:bg-blue-500 selection:text-white">

    <!-- Header -->
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

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-6 py-12 flex-grow w-full">
        <div class="text-center mb-12">
            <h1 class="text-4xl md:text-5xl font-black tracking-tight mb-4 bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                VoidX Discord Render Proxy
            </h1>
            <p class="text-slate-400 text-lg max-w-2xl mx-auto">
                Cloudflare engellerine takılmayan, mobil uygulamalar ve bot entegrasyonları için kesintisiz Render altyapısı.
            </p>
        </div>

        <!-- Endpoints Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
            <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-md hover:border-blue-500/40 transition-all group">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs font-mono bg-blue-500/10 text-blue-400 px-3 py-1 rounded-lg border border-blue-500/20">POST /api/discord</span>
                    <i class="fa-solid fa-comments text-slate-500 group-hover:text-blue-400 transition-colors"></i>
                </div>
                <h3 class="font-mono font-bold text-white text-lg mb-2">Discord Proxy Endpoint</h3>
                <p class="text-slate-400 text-sm">Sunucuları, kanalları listeler ve güvenli mesaj köprüsü sağlar.</p>
            </div>

            <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-md hover:border-emerald-500/40 transition-all group">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs font-mono bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-lg border border-emerald-500/20">GET</span>
                    <i class="fa-solid fa-heart-pulse text-slate-500 group-hover:text-emerald-400 transition-colors"></i>
                </div>
                <h3 class="font-mono font-bold text-white text-lg mb-2">Sistem Durumu</h3>
                <p class="text-slate-400 text-sm">VoidX API sağlık durumunu ve çalışma süresini denetler.</p>
            </div>
        </div>

        <!-- Etkileşimli Test Alanı -->
        <div class="bg-slate-900/40 border border-slate-800 rounded-3xl p-8 text-center backdrop-blur-md">
            <h3 class="text-xl font-bold mb-3 text-white">Sistem Test Et</h3>
            <p class="text-slate-400 text-sm mb-6">Aşağıdaki butona basarak elektrik simülasyonunu test edebilirsin.</p>
            
            <button onclick="triggerSparks(event)" class="electric-btn relative bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold px-8 py-4 rounded-2xl shadow-xl shadow-blue-500/20 cursor-pointer">
                <i class="fa-solid fa-bolt mr-2"></i> Sistemi Ateşle
            </button>
        </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <p>VoidX Studios © 2026 — Render Cloud Architecture</p>
    </footer>

    <!-- Elektrik / Parıltı Animasyon Scripti -->
    <script>
        function triggerSparks(e) {
            const btn = e.currentTarget;
            for (let i = 0; i < 12; i++) {
                const spark = document.createElement('div');
                spark.classList.add('spark');
                
                const angle = Math.random() * Math.PI * 2;
                const distance = 80 + Math.random() * 60;
                const startX = Math.cos(angle) * distance;
                const startY = Math.sin(angle) * distance;
                
                spark.style.width = (4 + Math.random() * 4) + 'px';
                spark.style.height = spark.style.width;
                spark.style.setProperty('--startX', startX + 'px');
                spark.style.setProperty('--startY', startY + 'px');
                
                btn.appendChild(spark);
                
                setTimeout(() => {
                    spark.classList.add('spark-active');
                }, 10);
                
                setTimeout(() => {
                    spark.remove();
                }, 400);
            }
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/discord", methods=["GET", "POST"])
def discord_proxy():
    if request.method == "GET":
        return jsonify({"status": "active", "brand": "VoidX Studios", "endpoint": "/api/discord"})

    try:
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

        # 1. Genel Bakış (Sunucular + Kanallar)
        if action == "overview":
            guilds_res = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
            if guilds_res.status_code != 200:
                return jsonify({
                    "error": "Discord sunucu listesini reddetti!",
                    "status_code": guilds_res.status_code,
                    "discord_response": guilds_res.text
                }), 400
            
            guilds = guilds_res.json()
            if not isinstance(guilds, list):
                return jsonify({"error": "Geçersiz veri formatı", "data": guilds}), 500

            overview_result = []
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
                            text_channels = [{"id": c.get("id"), "name": c.get("name")} for c in channels if c.get("type"] == 0 and c.get("id")]
                            if text_channels:
                                overview_result.append({"server_name": g_name, "channels": text_channels})
                    except:
                        pass

            # DM Kanalları
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

        # 2. Mesajları Oku
        elif action == "fetch":
            target_channel_id = channel_id
            if not target_channel_id:
                return jsonify({"error": "Lütfen Kanal ID girin."}), 400

            msg_res = requests.get(f"https://discord.com/api/v10/channels/{target_channel_id}/messages?limit=20", headers=headers)
            if msg_res.status_code != 200:
                return jsonify({"error": "Mesajlar çekilemedi.", "status_code": msg_res.status_code, "details": msg_res.text}), 400
            return jsonify(msg_res.json())

        # 3. Mesaj Gönder
        elif action == "send":
            if not channel_id or not content:
                return jsonify({"error": "Kanal ID ve mesaj gereklidir."}), 400
            res = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers=headers, json={"content": content})
            return jsonify(res.json()), res.status_code

        return jsonify({"error": "Geçersiz action."}), 400

    except Exception as err:
        return jsonify({"error": "Sunucu içi hata", "details": str(err)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
