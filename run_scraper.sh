#!/bin/bash
# -*- coding: utf-8 -*-
"""
Python 爬蟲執行腳本 - 使用 uv
方便快速執行各種爬蟲任務
"""

echo "🕷️ Hot Now 趨勢爬蟲 - Python 版本 (uv)"
echo "==============================================="

# 檢查 uv 是否安裝
if ! command -v uv &> /dev/null; then
    echo "❌ 錯誤: 未找到 uv"
    echo "請先安裝 uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 檢查是否在正確目錄
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 錯誤: 請在 trend-scraper-python 專案根目錄執行此腳本"
    echo "當前目錄: $(pwd)"
    exit 1
fi

echo "🔍 檢查專案環境..."
uv sync

if [ $? -ne 0 ]; then
    echo "❌ 依賴套件同步失敗"
    exit 1
fi

echo ""
echo "🚀 開始執行爬蟲..."
echo "==============================================="

# 根據參數執行對應的爬蟲
case "$1" in
    "google")
        echo "🔍 執行 Google 熱搜爬蟲"
        uv run python src/google_trends.py
        ;;
    "ptt")
        echo "📰 執行 PTT 熱門文章爬蟲"
        uv run python src/ptt_trends.py
        ;;
    "komica")
        echo "🎯 執行 Komica 熱門文章爬蟲"
        uv run python src/komica_trends.py
        ;;
    "reddit")
        echo "🔥 執行 Reddit 熱門文章爬蟲"
        uv run python src/reddit_trends.py
        ;;
    "bbc")
        echo "📰 執行 BBC 中文新聞爬蟲"
        uv run python src/bbc_trends.py
        ;;
    "all"|"")
        echo "🚀 執行所有爬蟲"
        uv run python src/main.py all
        ;;
    "help"|"-h"|"--help")
        echo "使用方法:"
        echo "  $0 [爬蟲類型]"
        echo ""
        echo "爬蟲類型:"
        echo "  google   - Google 熱搜爬蟲"
        echo "  ptt      - PTT 熱門文章爬蟲"
        echo "  komica   - Komica 熱門文章爬蟲"
        echo "  reddit   - Reddit 熱門文章爬蟲"
        echo "  bbc      - BBC 中文新聞爬蟲"
        echo "  all      - 執行所有爬蟲 (預設)"
        echo "  help     - 顯示此說明"
        exit 0
        ;;
    *)
        echo "❌ 未知的爬蟲類型: $1"
        echo "使用 '$0 help' 查看可用選項"
        exit 1
        ;;
esac

echo ""
echo "✅ 執行完成!"
echo "📁 爬取的資料儲存在 data/ 目錄中"
