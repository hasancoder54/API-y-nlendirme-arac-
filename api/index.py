from flask import Flask, render_template_string, request, jsonify, redirect
import difflib

app = Flask(__name__)

# Tanımlı geçerli endpoint'lerimiz
VALID_ENDPOINTS = {
    "/api/discord": "Discord proxy ve veri çekme endpoint'i",
    "/api/status": "Sistem durum ve sağlık kontrolü",
    "/api/info": "API versiyon ve kullanım kılavuzu"
}

# Şık, elektrik animasyonlu ve ikonlu HTML / Tailwind Arayüzü
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Proxy API & Dashboard</title>
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

        /* Etraftan merkeze gelen elektrik / parıltı simülasyonu */
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
                <span class="font-bold text-lg tracking-wide bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">QuantumBridge API</span>
            </div>
            <div class="flex items-center space-x-2 text-xs bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-3 py-1.5 rounded-full">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>Vercel Edge Aktif</span>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-6 py-12 flex-grow w-full">
        {% if is_error %}
        <!-- Hata / 404 Görünümü -->
        <div class="bg-slate-900/80 border border-rose-500/30 rounded-3xl p-8 md:p-12 shadow-2xl text-center relative overflow-hidden backdrop-blur-xl">
            <div class="absolute -top-24 -right-24 w-48 h-48 bg-rose-500/10 rounded-full blur-3xl"></div>
            
            <div class="w-20 h-20 mx-auto mb-6 rounded-2xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400 text-3xl shadow-inner">
                <i class="fa-solid fa-triangle-exclamation"></i>
            </div>
            
            <h1 class="text-3xl md:text-4xl font-extrabold tracking-tight mb-3 text-white">Aradığınız Sayfa Bulunamadı</h1>
            <p class="text-slate-400 mb-8 max-w-md mx-auto">Girdiğiniz URL (`{{ requested_path }}`) sistemimizde mevcut değil.</p>

            {% if suggested_path %}
            <div class="mb-8 p-4 bg-slate-950/60 border border-blue-500/30 rounded-2xl inline-block text-left w-full max-w-md">
                <div class="text-xs text-blue-400 font-medium mb-1"><i class="fa-solid fa-wand-magic-sparkles mr-1"></i> Akıllı Tahmin Edilen Endpoint:</div>
                <a href="{{ suggested_path }}" class="text-white font-mono hover:text-blue-400 transition-colors flex items-center justify-between">
                    <span>{{ suggested_path }}</span>
                    <i class="fa-solid fa-arrow-right text-sm text-blue-400"></i>
                </a>
            </div>
            {% endif %}

            <div>
                <a href="/" class="electric-btn inline-flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white font-medium px-8 py-3.5 rounded-xl shadow-lg shadow-blue-600/30 transition-all cursor-pointer" onclick="triggerSparks(event)">
                    <i class="fa-solid fa-house"></i>
                    <span>Ana Sayfaya Dön</span>
                </a>
            </div>
        </div>

        {% else %}
        <!-- Ana Sayfa Görünümü -->
        <div class="text-center mb-12">
            <h1 class="text-4xl md:text-5xl font-black tracking-tight mb-4 bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                Engelsiz Discord & Proxy Köprüsü
            </h1>
            <p class="text-slate-400 text-lg max-w-2xl mx-auto">
                Türkiye'deki kısıtlamaları aşmak için tasarlanmış yüksek performanslı Vercel tabanlı arka uç API sistemi.
            </p>
        </div>

        <!-- Endpoints Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
            <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-md hover:border-blue-500/40 transition-all group">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs font-mono bg-blue-500/10 text-blue-400 px-3 py-1 rounded-lg border border-blue-500/20">GET / POST</span>
                    <i class="fa-solid fa-comments text-slate-500 group-hover:text-blue-400 transition-colors"></i>
                </div>
                <h3 class="font-mono font-bold text-white text-lg mb-2">/api/discord</h3>
                <p class="text-slate-400 text-sm">Discord API entegrasyonu ve mesaj yönetim köprüsü.</p>
            </div>

            <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-md hover:border-emerald-500/40 transition-all group">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs font-mono bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-lg border border-emerald-500/20">GET</span>
                    <i class="fa-solid fa-heart-pulse text-slate-500 group-hover:text-emerald-400 transition-colors"></i>
                </div>
                <h3 class="font-mono font-bold text-white text-lg mb-2">/api/status</h3>
                <p class="text-slate-400 text-sm">Sunucunun sağlık durumunu ve çalışma süresini denetler.</p>
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
        {% endif %}
    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <p>Python Flask & Vercel Serverless Architecture</p>
    </footer>

    <!-- Elektrik / Parıltı Animasyon Scripti -->
    <script>
        function triggerSparks(e) {
            const btn = e.currentTarget;
            const rect = btn.getBoundingClientRect();
            
            // Buton etrafında 8 farklı yönden merkeze doğru elektrik kıvılcımları üret
            for (let i = 0; i < 12; i++) {
                const spark = document.createElement('div');
                spark.classList.add('spark');
                
                // Rastgele başlangıç pozisyonları (butonun etrafındaki alan)
                const angle = Math.random() * Math.PI * 2;
                const distance = 80 + Math.random() * 60;
                const startX = Math.cos(angle) * distance;
                const startY = Math.sin(angle) * distance;
                
                spark.style.width = (4 + Math.random() * 4) + 'px';
                spark.style.height = spark.style.width;
                spark.style.setProperty('--startX', startX + 'px');
                spark.style.setProperty('--startY', startY + 'px');
                
                btn.appendChild(spark);
                
                // Animasyonu tetikle
                setTimeout(() => {
                    spark.classList.add('spark-active');
                }, 10);
                
                // Süre bitince DOM'dan temizle
                setTimeout(() => {
                    spark.remove();
                }, 400);
            }
        }
    </script>
</body>
</html>
"""

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    full_path = "/" + path
    
    # Eğer ana sayfadaysa
    if full_path == "/":
        return render_template_string(HTML_TEMPLATE, is_error=False)
        
    # Eğer geçerli bir endpoint ise içeriğini döndür
    if full_path in VALID_ENDPOINTS:
        return jsonify({
            "endpoint": full_path,
            "description": VALID_ENDPOINTS[full_path],
            "status": "success",
            "message": "Endpoint aktif ve doğru çalışıyor."
        })
        
    # Yanlış URL girildiyse akıllı tahmin yap (difflib kullanarak)
    matches = difflib.get_close_matches(full_path, VALID_ENDPOINTS.keys(), n=1, cutoff=0.3)
    suggested_path = matches[0] if matches else "/"
    
    return render_template_string(
        HTML_TEMPLATE, 
        is_error=True, 
        requested_path=full_path, 
        suggested_path=suggested_path
    ), 404

if __name__ == "__main__":
    app.run(debug=True)
