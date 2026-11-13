from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import subprocess, sys, html
root = Path(__file__).resolve().parent
artifacts = Path.home()/'Library/CloudStorage/OneDrive-个人/资料/人工智能专业导论/.codex-lab3'
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  case = self.path.strip('/')
  if case not in ('1','2','3'):
   self.send_error(404); return
  result = subprocess.run([sys.executable, str(root/'expert_system.py'), case], capture_output=True, text=True)
  (artifacts/f'result-{case}.txt').write_text(result.stdout)
  page = '<!doctype html><meta charset="utf-8"><title>专家系统实验运行结果</title><style>body{margin:24px;background:white;color:#111;font:20px monospace}h1{font:600 24px sans-serif;margin:0 0 14px}pre{white-space:pre-wrap;line-height:1.45;margin:0}footer{margin-top:14px;font:16px sans-serif;color:#555}</style>'
  page += '<h1>专家系统实验 · Python 实际运行输出</h1><pre>'+html.escape(result.stdout)+'</pre><footer>进程退出码：'+str(result.returncode)+' | 命令：python3 expert_system.py '+case+'</footer>'
  self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.end_headers(); self.wfile.write(page.encode())
HTTPServer(('127.0.0.1',8766),Handler).serve_forever()
