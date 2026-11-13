#!/bin/zsh
set -e
cd "${0:A:h}"
source ./环境变量.sh
python ./验证环境.py
