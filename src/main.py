#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
熱門趨勢爬蟲主程式 - Python 版本
統一執行所有爬蟲任務
"""

import sys
import argparse
from pathlib import Path
from typing import Callable, List, Tuple

# 添加當前目錄到 Python 路徑
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# 導入各個爬蟲模組
try:
    from google_trends import main as google_main
    from ptt_trends import main as ptt_main
    from komica_trends import main as komica_main
    from reddit_trends import main as reddit_main
    from bbc_trends import main as bbc_main
except ImportError as e:
    print(f"❌ 導入爬蟲模組失敗: {e}")
    print("請確保已安裝所有依賴套件: uv sync")
    sys.exit(1)


def run_google_scraper() -> bool:
    """執行 Google 熱搜爬蟲"""
    print("🔍 執行 Google 熱搜爬蟲")
    print("=" * 50)
    try:
        google_main()
        print("✅ Google 熱搜爬蟲執行完成\n")
        return True
    except Exception as e:
        print(f"❌ Google 熱搜爬蟲執行失敗: {e}\n")
        return False

def run_ptt_scraper() -> bool:
    """執行 PTT 熱門文章爬蟲"""
    print("📰 執行 PTT 熱門文章爬蟲")
    print("=" * 50)
    try:
        ptt_main()
        print("✅ PTT 熱門文章爬蟲執行完成\n")
        return True
    except Exception as e:
        print(f"❌ PTT 熱門文章爬蟲執行失敗: {e}\n")
        return False


def run_komica_scraper() -> bool:
    """執行 Komica 熱門文章爬蟲"""
    print("🎯 執行 Komica(K島) 熱門文章爬蟲")
    print("=" * 50)
    try:
        komica_main()
        print("✅ Komica 熱門文章爬蟲執行完成\n")
        return True
    except Exception as e:
        print(f"❌ Komica 熱門文章爬蟲執行失敗: {e}\n")
        return False


def run_reddit_scraper() -> bool:
    """執行 Reddit 熱門文章爬蟲"""
    print("🔥 執行 Reddit 熱門文章爬蟲")
    print("=" * 50)
    try:
        reddit_main()
        print("✅ Reddit 熱門文章爬蟲執行完成\n")
        return True
    except Exception as e:
        print(f"❌ Reddit 熱門文章爬蟲執行失敗: {e}\n")
        return False


def run_bbc_scraper() -> bool:
    """執行 BBC 中文新聞爬蟲"""
    print("📰 執行 BBC 中文新聞爬蟲")
    print("=" * 50)
    try:
        bbc_main()
        print("✅ BBC 中文新聞爬蟲執行完成\n")
        return True
    except Exception as e:
        print(f"❌ BBC 中文新聞爬蟲執行失敗: {e}\n")
        return False


def run_all_scrapers() -> bool:
    """執行所有爬蟲"""
    print("🚀 執行所有爬蟲任務")
    print("=" * 60)
    
    scrapers = [
        ("Google 熱搜", run_google_scraper),
        ("PTT 熱門文章", run_ptt_scraper),
        ("Komica 熱門文章", run_komica_scraper),
        ("Reddit 熱門文章", run_reddit_scraper),
        ("BBC 中文新聞", run_bbc_scraper)
    ]
    
    results = []
    
    for name, scraper_func in scrapers:
        success = scraper_func()
        results.append((name, success))
    
    # 顯示總結
    print("=" * 60)
    print("📊 執行結果總結:")
    print("=" * 60)
    
    success_count = 0
    for name, success in results:
        status = "✅ 成功" if success else "❌ 失敗"
        print(f"{status} - {name}")
        if success:
            success_count += 1
    
    print("-" * 60)
    print(f"🎯 成功執行: {success_count}/{len(scrapers)} 個爬蟲")
    
    return success_count == len(scrapers)

def main() -> None:
    """主函數"""
    parser = argparse.ArgumentParser(description='熱門趨勢爬蟲 - Python 版本')
    parser.add_argument('scraper', nargs='?', choices=['google', 'ptt', 'komica', 'reddit', 'bbc', 'all'], 
                       default='all', help='選擇要執行的爬蟲 (預設: all)')
    
    args = parser.parse_args()
    
    print("🕷️ 熱門趨勢爬蟲 - Python 版本")
    print("🔗 GitHub: https://github.com/garylin0969/trend-scraper")
    print("🌐 Hot Now: https://hotnow.garylin.dev")
    print("=" * 60)
    
    if args.scraper == 'google':
        success = run_google_scraper()
    elif args.scraper == 'ptt':
        success = run_ptt_scraper()
    elif args.scraper == 'komica':
        success = run_komica_scraper()
    elif args.scraper == 'reddit':
        success = run_reddit_scraper()
    elif args.scraper == 'bbc':
        success = run_bbc_scraper()
    elif args.scraper == 'all':
        success = run_all_scrapers()
    else:
        print(f"❌ 未知的爬蟲類型: {args.scraper}")
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
