#!/bin/zsh
set -e
cd "${0:A:h}"
source ./环境变量.sh
"$NEO4J_HOME/bin/neo4j" stop
