
exec > /home/LogFiles/startup.log 2>&1

#!/bin/bash
set -e
set -x

handle_error() {
    echo "❌ Error at line: ${1}"
    echo "$(cat /tmp/last_command_output 2>/dev/null || echo 'No output')"
    exit 1
}
trap 'handle_error ${LINENO}' ERR

run_with_output() {
    "$@" > /tmp/last_command_output 2>&1
    cat /tmp/last_command_output
}

# パッケージインストール
run_with_output python3 -m pip install -r /home/site/wwwroot/requirements.txt

# DB接続確認
run_with_output python3 -c 'from models.database import engine; print("✅ DB connection successful")'

# FastAPIアプリ起動
exec gunicorn main:app \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind=0.0.0.0:8000 \
    --timeout 120
