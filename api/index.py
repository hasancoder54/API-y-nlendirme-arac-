from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QuantumBridge API</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between font-sans">
    <header class="border-b border-slate-800 bg-slate-900/50 p-6 flex justify-between items-center">
        <h1 class="font-bold text-lg text-blue-400"><i class="fa-solid fa-bolt-lightning mr-2"></i>QuantumBridge API Aktif</h1>
        <span class="text-xs bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full border border-emerald-500/30">Çalışıyor</span>
    </header>
    <main class="max-w-3xl mx-auto px-6 py-12 text-center flex-grow">
        <h2 class="text-3xl font-extrabold mb-4">Discord Proxy Sunucusu Hazır</h2>
        <p class="text-slate-400 mb-8">Özel domaininiz üzerinden VPN'siz Discord entegrasyonu aktif.</p>
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl text-left font-mono text-sm">
            <p class="text-blue-400 mb-2">// Endpoint:</p>
            <p class="text-slate-200">POST /api/discord</p>
        </div>
    </main>
    <footer class="border-t border-slate-900 py-4 text-center text-xs text-slate-600">Vercel Serverless Python</footer>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/discord", methods=["GET", "POST"])
def discord_proxy():
    if request.method == "GET":
        return jsonify({"status": "active", "endpoint": "/api/discord"})

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
            "User-Agent": "Mozilla/5.0"
        }

        if action == "overview":
            guilds_res = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
            if guilds_res.status_code != 200:
                return jsonify({"error": "Token geçersiz veya yetkisiz.", "details": guilds_res.text}), 400
            
            guilds = guilds_res.json()
            if not isinstance(guilds, list):
                return jsonify({"error": "Discord'dan geçersiz veri döndü."}), 500

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
                            text_channels = [{"id": c.get("id"), "name": c.get("name")} for c in channels if c.get("type") == 0 and c.get("id")]
                            overview_result.append({"server_name": g_name, "channels": text_channels})
                    except:
                        pass
            return jsonify(overview_result)

        elif action == "fetch":
            target_channel_id = channel_id
            if not target_channel_id:
                guilds_res = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
                if guilds_res.status_code != 200:
                    return jsonify({"error": "Sunucular alınamadı."}), 400
                guilds = guilds_res.json()
                if not guilds:
                    return jsonify({"error": "Sunucu bulunamadı."}), 400
                
                first_guild_id = guilds[0].get("id")
                channels_res = requests.get(f"https://discord.com/api/v10/guilds/{first_guild_id}/channels", headers=headers)
                if channels_res.status_code != 200:
                    return jsonify({"error": "Kanallar alınamadı."}), 400
                channels = channels_res.json()
                for c in channels:
                    if c.get("type") == 0:
                        target_channel_id = c.get("id")
                        break

            msg_res = requests.get(f"https://discord.com/api/v10/channels/{target_channel_id}/messages?limit=20", headers=headers)
            if msg_res.status_code != 200:
                return jsonify({"error": "Mesajlar çekilemedi.", "details": msg_res.text}), 400
            return jsonify(msg_res.json())

        elif action == "send":
            if not channel_id or not content:
                return jsonify({"error": "Kanal ID ve mesaj gereklidir."}), 400
            res = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers=headers, json={"content": content})
            return jsonify(res.json()), res.status_code

        return jsonify({"error": "Geçersiz action."}), 400

    except Exception as err:
        return jsonify({"error": "Sunucu hatası", "details": str(err)}), 500
