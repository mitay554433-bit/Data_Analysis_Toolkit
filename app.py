import os, time, json
from flask import Flask, request, jsonify

app = Flask(__name__)

# =========================
# CONFIG (simple gating)
# =========================
FREE_LIMIT_PER_DAY = 10
API_KEY = os.environ.get("API_KEY", "")  # optional for "pro"

# in-memory usage (replace with DB later)
USAGE = {}  # {ip: {day: count}}

def today():
    return time.strftime("%Y-%m-%d")

def is_allowed(ip):
    day = today()
    if ip not in USAGE:
        USAGE[ip] = {}
    if day not in USAGE[ip]:
        USAGE[ip][day] = 0
    return USAGE[ip][day] < FREE_LIMIT_PER_DAY

def inc(ip):
    day = today()
    USAGE[ip][day] += 1

def pro(req):
    key = req.headers.get("x-api-key", "")
    return API_KEY and key == API_KEY

# =========================
# TOOL ENGINES
# =========================
def tool_data(payload):
    s = len(str(payload))
    return {"tool":"data","score": s % 100, "summary": "basic data insight"}

def tool_log(payload):
    txt = str(payload).lower()
    errors = txt.count("error")
    return {"tool":"log","errors": errors, "status": "ok" if errors==0 else "issues found"}

def tool_file(payload):
    size = len(str(payload))
    return {"tool":"file","size": size, "advice": "compress" if size>50 else "ok"}

def tool_multi(payload):
    return {
        "tool":"multi",
        "data": tool_data(payload),
        "log": tool_log(payload),
        "file": tool_file(payload)
    }

TOOLS = {
    "data": tool_data,
    "log": tool_log,
    "file": tool_file,
    "multi": tool_multi
}

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return f"""
    <html>
    <head>
      <title>OMNISYS Platform</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body{{background:#0b1220;color:#e6edf3;font-family:Arial;margin:0;padding:20px}}
        .card{{background:#111827;border-radius:12px;padding:16px;margin-bottom:12px}}
        button{{padding:10px 14px;border:0;border-radius:8px;background:#2563eb;color:#fff;cursor:pointer}}
        select,input{{padding:10px;border-radius:8px;border:1px solid #1f2937;background:#020617;color:#e6edf3}}
        pre{{background:#020617;padding:12px;border-radius:8px;overflow:auto}}
      </style>
      <script>
        async function run(){
          const tool = document.getElementById('tool').value;
          const data = document.getElementById('data').value;
          const res = await fetch('/run', {{
            method:'POST',
            headers:{{'Content-Type':'application/json'}},
            body: JSON.stringify({{tool:tool, data:data}})
          }});
          const j = await res.json();
          document.getElementById('out').innerText = JSON.stringify(j,null,2);
        }
      </script>
    </head>
    <body>
      <div class="card">
        <h2>🚀 OMNISYS Platform</h2>
        <p>Tools: data • log • file • multi</p>
      </div>

      <div class="card">
        <select id="tool">
          <option value="data">data</option>
          <option value="log">log</option>
          <option value="file">file</option>
          <option value="multi">multi</option>
        </select>
        <input id="data" placeholder="paste input..." style="width:60%">
        <button onclick="run()">Run</button>
      </div>

      <div class="card">
        <pre id="out"></pre>
      </div>

      <div class="card">
        <p>Free: {FREE_LIMIT_PER_DAY} requests/day • Pro: unlimited</p>
      </div>
    </body>
    </html>
    """

@app.route("/run", methods=["POST"])
def run_tool():
    payload = request.json or {}
    tool = payload.get("tool","data")
    data = payload.get("data","")

    fn = TOOLS.get(tool)
    if not fn:
        return jsonify({"error":"invalid tool"}), 400

    ip = request.remote_addr or "anon"

    if not pro(request):
        if not is_allowed(ip):
            return jsonify({
                "error":"limit reached",
                "upgrade":"add x-api-key header for pro or purchase access"
            }), 402
        inc(ip)

    result = fn(data)

    # simple monetization hint
    tier = "pro" if (isinstance(result, dict) and result.get("tool")=="multi") else "basic"
    price = 49 if tier=="basic" else 149

    return jsonify({
        "result": result,
        "tier": tier,
        "price": price
    })

@app.route("/health")
def health():
    return jsonify({"status":"ok","time": time.time()})

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
