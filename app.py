import os
import sys
import traceback
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# VoidX Studios - Ultra Gelişmiş Elit Siber Neon Ana Sayfa
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoidX Studios | Elit Discord Proxy & Gateway Engine</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @keyframes cyberGlow {
            0% { box-shadow: 0 0 15px rgba(59, 130, 246, 0.4), inset 0 0 15px rgba(59, 130, 246, 0.2); }
            50% { box-shadow: 0 0 35px rgba(99, 102, 241, 0.8), inset 0 0 25px rgba(99, 102, 241, 0.4); }
            100% { box-shadow: 0 0 15px rgba(59, 130, 246, 0.4), inset 0 0 15px rgba(59, 130, 246, 0.2); }
        }
        .cyber-card { animation: cyberGlow 4s infinite ease-in-out; }
        .electric-btn { position: relative; overflow: hidden; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .electric-btn:active { transform: scale(0.96); }
        .spark { position: absolute; background: #38bdf8; pointer-events: none; opacity: 0; border-radius: 50%; box-shadow: 0 0 12px #38bdf8, 0 0 24px #6366f1; }
        @keyframes sparkAnim {
            0% { transform: translate(var(--startX), var(--startY)) scale(0.3); opacity: 1; }
            100% { transform: translate(0, 0) scale(1.8); opacity: 0; }
        }
        .spark-active { animation: sparkAnim 0.45s cubic-bezier(0.1, 0.8, 0.3, 1) forwards; }
        body { background-color: #030712; color: #f3f4f6; font-family: system-ui, -apple-system, sans-serif; }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-cyan-500 selection:text-slate-950">

    <!-- Header / Navbar -->
    <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-xl sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-600/30 border border-cyan-500/40 flex items-center justify-center text-cyan-400 shadow-xl shadow-cyan-500/10">
                    <i class="fa-solid fa-microchip text-xl"></i>
                </div>
                <div>
                    <span class="font-black text-xl tracking-wider bg-gradient-to-r from-cyan-400 via-blue-500 to-indigo-500 bg-clip-text text-transparent">VOIDX STUDIOS</span>
                    <span class="block text-[10px] text-slate-400 font-mono tracking-widest uppercase">Secure Enterprise Proxy Core</span>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <div class="hidden md:flex items-center space-x-2 text-xs bg-slate-900/90 border border-slate-700/80 text-cyan-400 px-4 py-2 rounded-xl font-mono shadow-inner">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
                    <span>SECURITY FIREWALL: ACTIVE</span>
                </div>
                <div class="text-xs bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 px-4 py-2 rounded-xl font-mono font-bold">
                    v4.8.2-PROD
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content Area -->
    <main class="max-w-5xl mx-auto px-6 py-16 flex-grow w-full">
        
        <!-- Hero Section -->
        <div class="text-center mb-16">
            <div class="inline-flex items-center space-x-2 bg-blue-500/10 border border-blue-500/20 text-blue-400 px-4 py-1.5 rounded-full text-xs font-mono mb-6 shadow-sm">
                <i class="fa-solid fa-shield-halved mr-1.5"></i> Destrüktif İşlem Koruması Devrede
            </div>
            <h1 class="text-4xl md:text-6xl font-black tracking-tight mb-6 bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
                Yüksek Güvenlikli Discord Gateway Köprüsü
            </h1>
            <p class="text-slate-400 text-lg max-w-2xl mx-auto leading-relaxed">
                VoidX Studios tarafından geliştirilen bu altyapı; mobil uygulamalarınız için tam korumalı, şifrelenmiş ve kesintisiz bir Discord API iletişim katmanı sunar.
            </p>
        </div>

        <!-- System Architecture Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            <div class="cyber-card bg-slate-900/50 border border-slate-800 rounded-3xl p-7 backdrop-blur-xl transition-all duration-300 hover:border-cyan-500/50">
                <div class="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-5 text-lg">
                    <i class="fa-solid fa-lock"></i>
                </div>
                <h3 class="font-bold text-white text-lg mb-2">Güvenlik Duvarı</h3>
                <p class="text-slate-400 text-sm leading-relaxed">Kanal silme, banlama gibi tehlikeli ve yıkıcı komutlar çekirdek seviyesinde engellenmiştir.</p>
            </div>

            <div class="cyber-card bg-slate-900/50 border border-slate-800 rounded-3xl p-7 backdrop-blur-xl transition-all duration-300 hover:border-blue-500/50">
                <div class="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-400 mb-5 text-lg">
                    <i class="fa-solid fa-bolt"></i>
                </div>
                <h3 class="font-bold text-white text-lg mb-2">Yüksek Hız (Proxy)</h3>
                <p class="text-slate-400 text-sm leading-relaxed">Render bulut sunucuları üzerinden Cloudflare engellerini tamamen bypas eden optimize yönlendirme.</p>
            </div>

            <div class="cyber-card bg-slate-900/50 border border-slate-800 rounded-3xl p-7 backdrop-blur-xl transition-all duration-300 hover:border-indigo-500/50">
                <div class="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 mb-5 text-lg">
                    <i class="fa-solid fa-terminal"></i>
                </div>
                <h3 class="font-bold text-white text-lg mb-2">Detaylı Tanı (Debug)</h3>
                <p class="text-slate-400 text-sm leading-relaxed">Hata durumlarında sistem mimarisini ve logları en ince detayına kadar raporlayan gelişmiş yapı.</p>
            </div>
        </div>

        <!-- Interactive Telemetry / Test Panel -->
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-3xl p-8 md:p-10 shadow-2xl backdrop-blur-2xl relative overflow-hidden">
            <div class="absolute -top-24 -right-24 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none"></div>
            
            <div class="flex items-center justify-between mb-6 pb-6 border-b border-slate-800">
                <div>
                    <h3 class="text-xl font-bold text-white flex items-center">
                        <i class="fa-solid fa-satellite-dish text-cyan-400 mr-3"></i> Telemetri & Sistem Durumu
                    </h3>
                    <p class="text-slate-400 text-xs mt-1">Sunucu aktif olarak istekleri dinlemektedir.</p>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span class="text-xs font-mono text-emerald-400 font-semibold">ONLINE</span>
                </div>
            </div>

            <div class="flex flex-col md:flex-row items-center justify-between gap-6">
                <div class="text-left font-mono text-xs text-slate-400 space-y-1.5 w-full md:w-auto bg-slate-950/60 p-4 rounded-2xl border border-slate-800">
                    <p><span class="text-cyan-400">Endpoint:</span> POST /api/discord</p>
                    <p><span class="text-cyan-400">Protokol:</span> HTTPS / REST TLS 1.3</p>
                    <p><span class="text-cyan-400">Güvenlik:</span> Strict Destructive Block Enabled</p>
                </div>
                <button onclick="triggerSparks(event)" class="electric-btn w-full md:w-auto bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold px-8 py-4 rounded-2xl shadow-xl shadow-cyan-500/20 cursor-pointer flex items-center justify-center space-x-3">
                    <i class="fa-solid fa-bolt text-lg"></i>
                    <span>Sistemi Test Et & Kıvılcım Çakar</span>
                </button>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950 py-8 text-center text-xs text-slate-500 font-mono">
        <p>VOIDX STUDIOS © 2026 — SECURE CLOUD GATEWAY INFRASTRUCTURE</p>
    </footer>

    <!-- Electric Spark Simulation Script -->
    <script>
        function triggerSparks(e) {
            const btn = e.currentTarget;
            for (let i = 0; i < 16; i++) {
                const spark = document.createElement('div');
                spark.classList.add('spark');
                const angle = Math.random() * Math.PI * 2;
                const distance = 90 + Math.random() * 80;
                spark.style.setProperty('--startX', (Math.cos(angle) * distance) + 'px');
                spark.style.setProperty('--startY', (Math.sin(angle) * distance) + 'px');
                spark.style.width = (4 + Math.random() * 4) + 'px';
                spark.style.height = spark.style.width;
                btn.appendChild(spark);
                setTimeout(() => spark.classList.add('spark-active'), 15);
                setTimeout(() => spark.remove(), 450);
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
    try:
        # Gelen istek gövdesini güvenli bir şekilde ayrıştır
        data = request.json or {}
        token = data.get("token")
        action = data.get("action")
        channel_id = data.get("channel_id")
        content = data.get("content")

        # 1. Güvenlik Denetimi: Token Doğrulama
        if not token or not isinstance(token, str) or len(token.strip()) < 10:
            return jsonify({
                "error": "VOIDX_SECURITY_AUTHENTICATION_FAILED",
                "status_code": 401,
                "description": "Gönderilen kimlik doğrulama token'ı geçersiz, boş veya eksik formatlı.",
                "diagnostic_trace": {
                    "provided_token_length": len(token) if token else 0,
                    "expected_format": "Bot <TOKEN> veya geçerli Discord kimlik dizgesi",
                    "timestamp": str(request.date) if hasattr(request, 'date') else "N/A"
                },
                "resolution_steps": [
                    "Uygulama içerisindeki token alanını kontrol edin.",
                    "Geçerli bir bot token değeri girdiğinizden emin olun."
                ]
            }), 401

        # 2. Güvenlik Duvarı: Yıkıcı (Destrüktif) İşlem Engeli
        # Kullanıcının kanal silme gibi zararlı istekler atmasını kesin olarak engelliyoruz.
        dangerous_actions = ["delete_channel", "delete", "ban", "kick", "purge", "remove_guild", "nuke"]
        if action in dangerous_actions or (isinstance(action, str) and "delete" in action.lower()):
            return jsonify({
                "error": "VOIDX_SECURITY_FIREWALL_BLOCK",
                "status_code": 403,
                "description": "VoidX Studios Güvenlik Duvarı: Bu API üzerinden kanal silme, sunucu yönetimi veya herhangi bir yıkıcı (destrüktif) işlem yapılması kesinlikle yasaktır ve engellenmiştir.",
                "diagnostic_trace": {
                    "blocked_action": action,
                    "target_channel": channel_id,
                    "security_rule": "SEC-POL-994: Destructive Operations Prohibited",
                    "client_ip": request.remote_addr
                },
                "resolution_steps": [
                    "Kanal silme veya sunucu değiştirme gibi işlemler bu arayüz üzerinden yapılamaz.",
                    "Sadece mesaj okuma ('fetch'), mesaj gönderme ('send') ve listeleme ('overview') işlemlerini kullanabilirsiniz."
                ]
            }), 403

        auth_token = token.strip()
        auth_header = auth_token if auth_token.startswith("Bot ") or auth_token.startswith("Bearer ") else f"Bot {auth_token}"
        
        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 VoidXGateway/4.8"
        }

        # 3. İşlem Modülü: Overview (Sunucular ve Kanallar)
        if action == "overview":
            overview_result = []
            guilds_res = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers, timeout=10)
            
            if guilds_res.status_code != 200:
                return jsonify({
                    "error": "VOIDX_DISCORD_API_GUILDS_REJECTED",
                    "status_code": guilds_res.status_code,
                    "description": "Discord API, sunucu listesi çekme isteğini reddetti. Token yetkileri yetersiz olabilir.",
                    "diagnostic_trace": {
                        "discord_http_status": guilds_res.status_code,
                        "raw_discord_response": guilds_res.text,
                        "auth_type_used": auth_header.split()[0]
                    },
                    "resolution_steps": [
                        "Botunuzun sunuculara 'View Channels' yetkisiyle eklendiğinden emin olun.",
                        "Kullandığınız token değerinin geçerliliğini doğrulayın."
                    ]
                }), 400
            
            guilds = guilds_res.json()
            if isinstance(guilds, list):
                for g in guilds:
                    g_id = g.get("id")
                    g_name = g.get("name")
                    if not g_id:
                        continue
                    
                    ch_res = requests.get(f"https://discord.com/api/v10/guilds/{g_id}/channels", headers=headers, timeout=8)
                    if ch_res.status_code == 200:
                        try:
                            channels = ch_res.json()
                            if isinstance(channels, list):
                                text_channels = [{"id": c.get("id"), "name": c.get("name")} for c in channels if c.get("type") == 0 and c.get("id")]
                                overview_result.append({"server_name": g_name, "channels": text_channels if text_channels else [{"id": "0", "name": "Metin kanalı bulunamadı"}]})
                        except Exception as parse_ex:
                            overview_result.append({"server_name": g_name, "channels": [{"id": "0", "name": f"Parse Hatası: {str(parse_ex)}"}]})
                    else:
                        overview_result.append({"server_name": g_name, "channels": [{"id": "0", "name": f"Erişim Engellendi (Status: {ch_res.status_code})"}]})

            # DM Kanalları Entegrasyonu
            dm_res = requests.get("https://discord.com/api/v10/users/@me/channels", headers=headers, timeout=8)
            if dm_res.status_code == 200:
                dm_channels = dm_res.json()
                if isinstance(dm_channels, list) and dm_channels:
                    dm_list = [{"id": dm.get("id"), "name": f"DM Sohbet ({dm.get('id')})"} for dm in dm_channels]
                    overview_result.append({"server_name": "Özel Mesajlar (DM)", "channels": dm_list})

            if not overview_result:
                return jsonify({
                    "error": "VOIDX_NO_ACCESSIBLE_CHANNELS_FOUND",
                    "status_code": 404,
                    "description": "Hesaba veya bota bağlı erişilebilir hiçbir sunucu veya kanal tespit edilemedi.",
                    "diagnostic_trace": {
                        "guilds_count": len(guilds) if isinstance(guilds, list) else 0,
                        "dm_status": dm_res.status_code
                    },
                    "resolution_steps": ["Botunuzu en az bir Discord sunucusuna davet edin."]
                }), 404

            return jsonify(overview_result)

        # 4. İşlem Modülü: Fetch (Mesaj Okuma)
        elif action == "fetch":
            if not channel_id:
                return jsonify({
                    "error": "VOIDX_MISSING_CHANNEL_ID",
                    "status_code": 400,
                    "description": "Mesajları okuyabilmek için geçerli bir 'channel_id' parametresi zorunludur.",
                    "diagnostic_trace": {"provided_channel_id": channel_id},
                    "resolution_steps": ["Uygulama içerisindeki Kanal ID kutucuğuna hedef kanalın kimliğini girin."]
                }), 400
            
            msg_res = requests.get(f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=20", headers=headers, timeout=10)
            if msg_res.status_code != 200:
                return jsonify({
                    "error": "VOIDX_DISCORD_FETCH_FAILED",
                    "status_code": msg_res.status_code,
                    "description": "Discord API, belirtilen kanaldaki mesajları okuma isteğini geri çevirdi.",
                    "diagnostic_trace": {
                        "target_channel": channel_id,
                        "discord_status": msg_res.status_code,
                        "discord_error_details": msg_res.text
                    },
                    "resolution_steps": [
                        "Botun ilgili kanalı görme (View Channel) ve mesaj geçmişini okuma (Read Message History) yetkisi olduğundan emin olun.",
                        "Kanal ID numarasını doğru yazıp yazmadığınızı kontrol edin."
                    ]
                }), 400
            return jsonify(msg_res.json())

        # 5. İşlem Modülü: Send (Mesaj Gönderme)
        elif action == "send":
            if not channel_id or not content:
                return jsonify({
                    "error": "VOIDX_MISSING_PAYLOAD_DATA",
                    "status_code": 400,
                    "description": "Mesaj göndermek için hem 'channel_id' hem de 'content' (mesaj içeriği) alanları zorunludur.",
                    "diagnostic_trace": {
                        "channel_id_provided": bool(channel_id),
                        "content_provided": bool(content)
                    },
                    "resolution_steps": ["Mesaj kutusuna bir şeyler yazdığınızdan ve kanal ID seçtiğinizden emin olun."]
                }), 400
            
            res = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers=headers, json={"content": content}, timeout=10)
            if res.status_code not in [200, 201]:
                return jsonify({
                    "error": "VOIDX_DISCORD_SEND_FAILED",
                    "status_code": res.status_code,
                    "description": "Discord API mesajın iletilmesini reddetti.",
                    "diagnostic_trace": {
                        "target_channel": channel_id,
                        "discord_status": res.status_code,
                        "discord_error_details": res.text
                    },
                    "resolution_steps": ["Botun bu kanala mesaj yazma (Send Messages) yetkisi olduğunu doğrulayın."]
                }), res.status_code

            return jsonify(res.json()), res.status_code

        # Tanımsız İşlem Hatası
        return jsonify({
            "error": "VOIDX_INVALID_ACTION_PARAMETER",
            "status_code": 400,
            "description": f"Geçersiz veya desteklenmeyen action değeri: '{action}'.",
            "diagnostic_trace": {"received_action": action},
            "resolution_steps": ["Desteklenen action parametreleri: overview, fetch, send"]
        }), 400

    except Exception as err:
        # Aşırı detaylı istisna (exception) raporlama bloğu
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_list = traceback.format_tb(exc_tb)
        detailed_traceback = "".join(tb_list)
        
        return jsonify({
            "error": "VOIDX_INTERNAL_SERVER_CRITICAL_EXCEPTION",
            "status_code": 500,
            "description": "VoidX proxy sunucusunda yürütme sırasında beklenmeyen kritik bir hata oluştu.",
            "diagnostic_trace": {
                "exception_type": str(exc_type.__name__),
                "exception_message": str(err),
                "stack_trace": detailed_traceback
            },
            "resolution_steps": [
                "Lütfen bu hata logunu VoidX Studios geliştirici ekibine iletin.",
                "Gelen istek JSON gövdesinin doğru formatta olduğundan emin olun."
            ]
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
