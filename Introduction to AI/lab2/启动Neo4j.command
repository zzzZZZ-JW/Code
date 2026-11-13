#!/bin/zsh
set -e
cd "${0:A:h}"
source ./环境变量.sh
if ! "$NEO4J_HOME/bin/neo4j" status; then
    "$NEO4J_HOME/bin/neo4j" start
fi
for attempt in {1..60}; do
    if curl -fsS http://localhost:7474/ >/dev/null; then
        open http://localhost:7474/browser/
        printf '\n浏览器已打开。用户名 neo4j；双击“查看登录信息.command”查看密码。\n'
        exit 0
    fi
    sleep 1
done
printf '启动超时，请检查 %s/logs/neo4j.log\n' "$NEO4J_HOME"
exit 1
