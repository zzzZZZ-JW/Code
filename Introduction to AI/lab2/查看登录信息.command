#!/bin/zsh
"$HOME/.local/share/ai-intro-lab2/venv/bin/python" - <<'PY'
from pathlib import Path
import json
c = json.loads((Path.home()/'.local/share/ai-intro-lab2/connection.json').read_text())
print('浏览器：http://localhost:7474/browser/')
print('连接地址：', c['uri'])
print('用户名：', c['user'])
print('密码：', c['password'])
PY
