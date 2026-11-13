from pathlib import Path
import json
import platform
import subprocess
import urllib.request
import uuid
import pandas as pd
import py2neo
from py2neo import Graph, Node, Relationship

BASE = Path.home() / '.local/share/ai-intro-lab2'
JAVA_HOME = Path('/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home')
config = json.loads((BASE / 'connection.json').read_text())
print(subprocess.run([str(JAVA_HOME / 'bin/java'), '-version'], capture_output=True, text=True, check=True).stderr.strip())
print(f'Python {platform.python_version()} | py2neo {py2neo.__version__} | pandas {pd.__version__}')
with urllib.request.urlopen('http://localhost:7474/browser/', timeout=10) as response:
    assert response.status == 200
print('PASS: Neo4j Browser HTTP 200')
graph = Graph(config['uri'], auth=(config['user'], config['password']))
print('Neo4j:', graph.run('CALL dbms.components() YIELD name, versions, edition RETURN name, versions, edition').data())
assert graph.run('RETURN 1 AS ok').evaluate() == 1
print('PASS: Python Bolt authentication and Cypher query')
token = uuid.uuid4().hex
csv = BASE / 'neo4j-community-5.18.0/import' / f'environment-check-{token}.csv'
try:
    pd.DataFrame([{'id': 1, 'name': '中文环境验证'}]).to_csv(csv, index=False, encoding='utf-8')
    assert pd.read_csv(csv).iloc[0]['name'] == '中文环境验证'
    rows = graph.run('LOAD CSV WITH HEADERS FROM $url AS row RETURN row.name AS name', url=f'file:///{csv.name}').data()
    assert rows == [{'name': '中文环境验证'}]
    print('PASS: pandas UTF-8 CSV and Neo4j LOAD CSV')
    tx = graph.begin()
    try:
        a = Node('EnvironmentCheck', name='中文节点甲', test_id=token)
        b = Node('EnvironmentCheck', name='中文节点乙', test_id=token)
        tx.create(Relationship(a, 'CHECKS', b, order=1))
        assert tx.run('MATCH (a:EnvironmentCheck {test_id:$token})-[r:CHECKS]->(b) RETURN a.name, b.name, r.order', token=token).data() == [{'a.name':'中文节点甲','b.name':'中文节点乙','r.order':1}]
        tx.run('MATCH (n:EnvironmentCheck {test_id:$token}) SET n.verified=true', token=token)
        assert tx.run('MATCH (n:EnvironmentCheck {test_id:$token, verified:true}) RETURN count(n)', token=token).evaluate() == 2
        tx.run('MATCH (n:EnvironmentCheck {test_id:$token}) DETACH DELETE n', token=token)
        assert tx.run('MATCH (n:EnvironmentCheck {test_id:$token}) RETURN count(n)', token=token).evaluate() == 0
    finally:
        graph.rollback(tx)
    print('PASS: py2neo node/relationship create, read, update, delete; transaction rolled back')
finally:
    csv.unlink(missing_ok=True)
assert graph.run('MATCH (n:EnvironmentCheck {test_id:$token}) RETURN count(n)', token=token).evaluate() == 0
print('PASS: no verification data retained')
print('环境验证全部通过。')
