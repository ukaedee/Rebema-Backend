#!/bin/bash
set -x  # デバッグ用出力

# タイムアウト設定（秒）
DB_CHECK_TIMEOUT=30

# エラーハンドリング関数
handle_error() {
    echo "Error occurred in script at line: ${1}"
    echo "Last command exit status: $?"
    echo "Last command output:"
    echo "$(cat /tmp/last_command_output 2>/dev/null || echo 'No output available')"
    exit 1
}
trap 'handle_error ${LINENO}' ERR

# コマンド出力を一時ファイルに保存する関数
run_with_output() {
    "$@" > /tmp/last_command_output 2>&1
    cat /tmp/last_command_output
}

# パッケージのインストール確認
run_with_output python3 -m pip install -r requirements.txt

# DB接続確認（例: MySQL用）
run_with_output python3 -c 'from models.database import engine; print("✅ DB connection successful")'

# Gunicorn + UvicornでFastAPIアプリ起動
exec gunicorn main:app \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind=0.0.0.0:8000 \
    --timeout 120

