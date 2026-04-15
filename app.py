import os, json, datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# =========================
# CORE SYSTEM STATE
# =========================
STATE = {
    "version": "EcoPIVOT.v1",
    "timestamp": lambda: datetime.datetime.utcnow().isoformat(),
    "modules": ["ingest","analyze","monetize"],
    "status": "LIVE"
}

# =========================
# UI (Dashboard)
# =========================
@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>OMNISYS • Data Analysis Toolkit</title>
        <style>
            body {{
                background:#0b1220;
                color:#e6edf3;
                font-family:Arial;
                margin:0;
                padding:40px;
            }}
            .card {{
                background:#111827;
                padding:20px;
                border-radius:12px;
                margin-bottom:20px;
                box-shadow:0 0 20px rgba(0,0,0,0.4);
            }}
            h1 {{margin:0 0 10px}}
            button {{
                padding:10px 15px;
                background:#2563eb;
                border:none;
                color:white;
                border-radius:6px;
                cursor:pointer;
            }}
        </style>
        <script>
            async function analyze(){
                let res = await fetch('/analyze', {{
                    method:'POST',
                    headers:{{'Content-Type':'application/json'}},
                    body: JSON.stringify({{data:"sample input"}})
                }});
                let d = await res.json();
                document.getElementById("out").innerText = JSON.stringify(d,null,2);
            }
        </script>
    </head>
    <body>
        <div class="card">
            <h1>🚀 OMNISYS Dashboard</h1>
            <p>Status: {STATE["status"]}</p>
            <p>Modules: {", ".join(STATE["modules"])}</p>
        </div>

        <div class="card">
            <h2>Run Analysis</h2>
            <button onclick="analyze()">Execute</button>
            <pre id="out"></pre>
        </div>
    </body>
    </html>
    """

# =========================
# INGEST ENGINE
# =========================
def ingest(payload):
    return {
        "ingested": payload,
        "ts": STATE["timestamp"]()
    }

# =========================
# ANALYSIS ENGINE
# =========================
def analyze(data):
    score = len(str(data)) % 100
    return {
        "score": score,
        "classification": "high" if score > 50 else "low"
    }

# =========================
# MONETIZATION ENGINE
# =========================
def monetize(result):
    tier = "pro" if result["score"] > 70 else "basic"
    price = 149 if tier == "pro" else 49
    return {"tier": tier, "price": price}

# =========================
# API ROUTES
# =========================
@app.route("/analyze", methods=["POST"])
def api_analyze():
    payload = request.json or {}

    ing = ingest(payload)
    res = analyze(ing)
    monet = monetize(res)

    return jsonify({
        "pipeline": {
            "ingest": ing,
            "analysis": res,
            "monetization": monet
        }
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "time": STATE["timestamp"]()
    })

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
