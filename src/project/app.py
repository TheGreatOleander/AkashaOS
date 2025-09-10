"""Simple heartbeat UI for AkashaOS - Hacker eyecandy front page."""
from flask import Flask, render_template_string, jsonify
import datetime, os, platform

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>AkashaOS — AetherBox</title>
  <style>
    body{background:#0f1724;color:#e6eef8;font-family:Inter,ui-sans-serif,system-ui,Segoe UI,Roboto,Helvetica,Arial;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
    .card{width:880px;max-width:94%;padding:28px;border-radius:16px;box-shadow:0 10px 30px rgba(2,6,23,0.6);background:linear-gradient(135deg,rgba(12,18,30,0.85),rgba(5,8,12,0.7));border:1px solid rgba(255,255,255,0.04)}
    h1{margin:0;font-size:28px;letter-spacing:0.6px}
    .meta{color:#99a3b2;margin-top:8px;font-size:13px}
    .grid{display:flex;gap:12px;margin-top:18px;flex-wrap:wrap}
    .box{flex:1 1 210px;padding:12px;border-radius:10px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.02)}
    .pulse{display:inline-block;height:10px;width:10px;background:#28c76f;border-radius:50%;box-shadow:0 0 12px #28c76f}
    pre{white-space:pre-wrap;word-break:break-word;color:#cfe6ff;background:rgba(0,0,0,0.12);padding:10px;border-radius:8px;font-size:13px}
    .logo{font-family:monospace;color:#7ce3ff;font-weight:700}
  </style>
</head>
<body>
<div class=card>
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div>
      <div class=logo>AkashaOS</div>
      <h1>Akasha AetherBox — heartbeat</h1>
      <div class=meta>Symbiotic OS • Cloud-ready • Hacker eyecandy</div>
    </div>
    <div style="text-align:right">
      <div class=pulse></div>
      <div class=meta id="time">{{ time }}</div>
    </div>
  </div>

  <div class=grid>
    <div class=box>
      <strong>Vitals</strong>
      <pre id="vitals">{{ vitals }}</pre>
    </div>
    <div class=box>
      <strong>Modules</strong>
      <pre id="modules">{{ modules }}</pre>
    </div>
    <div class=box>
      <strong>Recent Dream</strong>
      <pre id="dream">{{ dream }}</pre>
    </div>
  </div>
</div>
<script>
  async function refresh(){
    try {
      let r = await fetch('/api/status');
      let j = await r.json();
      document.getElementById('vitals').textContent = j.vitals;
      document.getElementById('modules').textContent = j.modules;
      document.getElementById('dream').textContent = j.dream;
      document.getElementById('time').textContent = j.time;
    } catch(e) { console.error(e) }
  }
  setInterval(refresh, 3000);
  refresh();
</script>
</body>
</html>
"""

@staticmethod
def _dummy(): pass
