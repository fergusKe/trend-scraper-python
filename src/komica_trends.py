#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Komica(K島) 熱門文章爬蟲 - Python 版本
爬取 K島 今日熱門文章 Top 50
"""

import json
import time
import random
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

def setup_driver():
    """設定 Chrome WebDriver"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-setuid-sandbox')
    
    # 使用隨機 User-Agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f'--user-agent={user_agent}')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

def parse_komica_line(line: str, base_url: str = "https://gita.komica1.org/00b/pixmicat.php?res=") -> Optional[Dict]:
    """解析 Komica 文章行資料"""
    try:
        # 移除行尾的"在新分頁開啟"文字
        line = line.replace('在新分頁開啟', '').strip()
        
        # 分割資料 - 格式: 回覆數|ID|日期|時間|標題|描述
        parts = line.split('|')
        
        if len(parts) >= 6:
            reply_count_str = parts[0].strip()
            thread_id = parts[1].strip()
            date = parts[2].strip()
            time = parts[3].strip()
            title = parts[4].strip()
            description = parts[5].strip()
            
            # 轉換回覆數為整數
            try:
                reply_count = int(reply_count_str)
            except ValueError:
                reply_count = 0
            
            # 建構完整連結
            link = f"{base_url}{thread_id}"
            
            return {
                "replyCount": reply_count,
                "date": date,
                "time": time,
                "title": title,
                "description": description,
                "link": link,
                "rawText": line  # 保留原始文字以備查看
            }
            
    except Exception as e:
        print(f"⚠️ 解析行資料時出錯: {e}")
        print(f"問題行: {line}")
    
    return None

def scrape_komica_trends():
    """爬取 Komica 熱門文章"""
    driver = setup_driver()
    trends = []
    
    try:
        print("🚀 開始爬取 Komica 熱門文章...")
        
        # 前往 Komica 頁面
        driver.get('https://gita.komica1.org/00b/catlist.php')
        
        print("⏳ 載入網頁...")
        
        # 等待 pre 標籤載入
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "pre"))
            )
            print("✅ 找到 pre 標籤")
        except TimeoutException:
            print("⚠️ 等待 pre 元素載入超時")
        
        # 找到所有 pre 標籤
        pre_elements = driver.find_elements(By.TAG_NAME, "pre")
        print(f"找到 pre 標籤數量: {len(pre_elements)}")
        
        # 找到包含今日熱門的 pre 標籤
        today_threads_pre = None
        for i, pre in enumerate(pre_elements):
            pre_text = pre.text
            if "今日熱門討論串 Top50" in pre_text:
                today_threads_pre = pre
                print(f"✅ 在第 {i+1} 個 pre 標籤中找到今日熱門討論串")
                break
        
        if not today_threads_pre:
            print("❌ 未找到包含今日熱門討論串的 pre 標籤")
            return []
        
        # 解析內容
        print("🔍 開始解析今日熱門討論串內容...")
        content = today_threads_pre.text
        
        # 按行分割
        lines = content.split('\n')
        
        # 找到包含熱門討論串資料的行
        data_lines = []
        in_data_section = False
        
        for line in lines:
            line = line.strip()
            
            # 跳過空行
            if not line:
                continue
            
            # 檢查是否進入資料區段
            if "今日熱門討論串 Top50" in line:
                in_data_section = True
                continue
            
            # 如果在資料區段且行包含 '|' 分隔符
            if in_data_section and '|' in line:
                # 確保這是有效的資料行（包含數字|ID|日期格式）
                if re.match(r'^\d+\|', line):
                    data_lines.append(line)
        
        print(f"📊 找到 {len(data_lines)} 行討論串資料")
        
        # 解析每一行資料
        for i, line in enumerate(data_lines):
            trend_data = parse_komica_line(line)
            if trend_data:
                trends.append(trend_data)
                print(f"✅ 第 {len(trends)} 篇: {trend_data['title'][:40]}...")
            else:
                print(f"⚠️ 無法解析第 {i+1} 行: {line[:50]}...")
        
    except Exception as e:
        print(f"❌ 爬取過程中出錯: {e}")
    
    finally:
        driver.quit()
    
    return trends

def save_komica_data(trends):
    """儲存 Komica 資料到 JSON 檔案"""
    data = {
        "updated": datetime.now().isoformat() + "Z",
        "trends": trends
    }
    
    # 確保 data 資料夾存在
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # 寫入 JSON 檔案
    output_file = data_dir / "komica-trends.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 資料已儲存至: {output_file}")
    return output_file

def main():
    """主函數"""
    print("🎯 Komica(K島) 熱門文章爬蟲 - Python 版本")
    print("=" * 50)
    
    # 爬取資料
    trends = scrape_komica_trends()
    
    if trends:
        # 儲存資料
        save_komica_data(trends)
        
        # 顯示結果摘要
        print("✅ 爬取完成!")
        print(f"📊 總共找到 {len(trends)} 篇熱門文章")
        
        # 顯示前幾篇文章標題
        for i, trend in enumerate(trends[:5], 1):
            print(f"{i}. [{trend.get('replyCount', 0)} 回覆] {trend.get('title', 'N/A')[:50]}...")
    else:
        print("❌ 沒有找到任何熱門文章")

if __name__ == "__main__":
    main()
