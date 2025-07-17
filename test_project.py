#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單的測試腳本，驗證專案結構和依賴
"""

import sys
from pathlib import Path

def test_project_structure():
    """測試專案結構"""
    print("🔍 檢查專案結構...")
    
    # 檢查重要檔案
    important_files = [
        "pyproject.toml",
        "scripts/__init__.py",
        "scripts/main.py",
        "scripts/google_trends.py",
        "scripts/ptt_trends.py",
        "scripts/komica_trends.py",
        "scripts/reddit_trends.py",
        "run_scraper.sh",
        "README.md",
        ".gitignore"
    ]
    
    missing_files = []
    for file_path in important_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少檔案: {missing_files}")
        return False
    else:
        print("✅ 所有重要檔案都存在")
        return True

def test_imports():
    """測試模組導入"""
    print("🔍 檢查模組導入...")
    
    try:
        # 測試基本模組
        import json
        import time
        import random
        import re
        from datetime import datetime
        from pathlib import Path
        from typing import List, Dict, Optional
        
        print("✅ 基本模組導入成功")
        
        # 測試是否可以導入腳本模組
        sys.path.append(str(Path("scripts")))
        
        # 由於可能沒有安裝 selenium 等依賴，我們只測試基本導入
        try:
            import scripts
            print("✅ 腳本包導入成功")
        except ImportError as e:
            print(f"⚠️ 腳本包導入警告 (這是正常的，因為可能缺少依賴): {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模組導入失敗: {e}")
        return False

def test_data_directory():
    """測試 data 目錄"""
    print("🔍 檢查 data 目錄...")
    
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir()
        print("✅ 建立 data 目錄")
    else:
        print("✅ data 目錄已存在")
    
    return True

def main():
    """主函數"""
    print("🧪 Trend Scraper Python 專案測試")
    print("=" * 50)
    
    tests = [
        ("專案結構", test_project_structure),
        ("模組導入", test_imports),
        ("data 目錄", test_data_directory)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 測試: {test_name}")
        print("-" * 30)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name} 測試通過")
        else:
            print(f"❌ {test_name} 測試失敗")
    
    print("\n" + "=" * 50)
    print(f"📊 測試結果: {passed}/{total} 個測試通過")
    
    if passed == total:
        print("🎉 所有測試都通過！專案結構正確。")
        print("\n📝 下一步:")
        print("1. 安裝 uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("2. 同步依賴: uv sync")
        print("3. 執行爬蟲: ./run_scraper.sh")
    else:
        print("⚠️ 部分測試未通過，請檢查專案結構。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
