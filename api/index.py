from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

@app.route("/api/discord", methods=["GET", "POST"])
def discord_proxy():
    if request.method == "POST":
        data = request.json or {}
        token = data.get("token")
        action = data.get("action")  # 'overview' veya 'fetch'
        channel_id = data.get("channel_id")
        content = data.get("content")

        if not token:
            return jsonify({"error": "Token zorunludur."}), 400

        auth_header = token if token.startswith("Bot ") or token.startswith("Bearer ") else f"Bot {token}"
        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        # 1. Genel Bakış: Tüm sunucuları ve içindeki kanalları otomatik listele
        if action == "overview":
            guilds_res = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
            if guilds_res.status_code != 200:
                return jsonify({"error": "Sunucular alınamadı, token'ı kontrol edin.", "details": guilds_res.json()}), 400
            
            guilds = guilds_res.json()
            overview_result = []

            for g in guilds:
                g_id = g["id"]
                g_name = g["name"]
                ch_res = requests.get(f"https://discord.com/api/v10/guilds/{g_id}/channels", headers=headers)
                if ch_res.status_code == 200:
                    channels = ch_res.json()
                    # Sadece metin kanallarını al (type 0)
                    text_channels = [{"id": c["id"], "name": c["name"]} for c in channels if c.get("type") == 0]
                    overview_result.append({
                        "server_name": g_name,
                        "channels": text_channels
                    })

            return jsonify(overview_result)

        # 2. Kanal ID verilmediyse otomatik ilk kanaldan mesajları çek
        if action == "fetch" and not channel_id:
            guilds_res = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
            if guilds_res.status_code != 200:
                return jsonify({"error": "Sunucular alınamadı."}), 400
            guilds = guilds_res.json()
            if not guilds:
                return jsonify({"error": "Hiçbir sunucu bulunamadı."}), 400

            first_guild_id = guilds[0]["id"]
            channels_res = requests.get(f"https://discord.com/api/v10/guilds/{first_guild_id}/channels", headers=headers)
            if channels_res.status_code != 200:
                return jsonify({"error": "Kanallar alınamadı."}), 400
            
            channels = channels_res.json()
            text_channel_id = None
            for c in channels:
                if c.get("type") == 0:
                    text_channel_id = c["id"]
                    break

            if not text_channel_id:
                return jsonify({"error": "Metin kanalı bulunamadı."}), 400
            
            channel_id = text_channel_id

        # 3. Mesaj Gönderme
        if action == "send":
            if not channel_id or not content:
                return jsonify({"error": "Kanal veya mesaj eksik."}), 400
            res = requests.post(
                f"https://discord.com/api/v10/channels/{channel_id}/messages",
                headers=headers,
                json={"content": content}
            )
            return jsonify(res.json()), res.status_code

        # 4. Mesajları Okuma
        if action == "fetch":
            res = requests.get(
                f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=20",
                headers=headers
            )
            return jsonify(res.json()), res.status_code

        return jsonify({"error": "Geçersiz işlem."}), 400

    return "Discord Proxy API Aktif"

if __name__ == "__main__":
    app.run(debug=True)
