#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google 熱搜爬蟲 - Python 版本
爬取台灣 Google 熱搜榜資料
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


def setup_driver() -> webdriver.Chrome:
    """設定 Chrome WebDriver"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-setuid-sandbox')
    
    # 使用隨機 User-Agent
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'--user-agent={user_agent}')
    
    # 自動下載並安裝最新的 ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver


def random_delay(min_seconds: float = 3, max_seconds: float = 13) -> None:
    """隨機延遲"""
    delay = random.uniform(min_seconds, max_seconds)
    print(f"⏳ 隨機延遲 {delay:.2f} 秒...")
    time.sleep(delay)


def scrape_google_trends() -> List[Dict[str, str]]:
    """爬取 Google 熱搜資料"""
    driver = setup_driver()
    trends = []
    
    try:
        print("🚀 開始爬取 Google 熱搜...")
        
        # 隨機延遲避免被偵測
        random_delay(3, 13)
        
        # 前往 Google 趨勢頁面
        driver.get('https://trends.google.com.tw/trending?geo=TW&hours=4')
        
        # 頁面載入後再次延遲
        random_delay(3, 8)
        
        # 等待表格載入
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "td"))
            )
            print("✅ 頁面載入完成")
        except TimeoutException:
            print("⚠️ 等待元素載入超時")
        
        # 找到所有表格行
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f"📊 找到 {len(rows)} 個表格行")
        
        # 過濾出有效的資料行（包含超過3個cell的行）
        data_rows = [row for row in rows if len(row.find_elements(By.TAG_NAME, "td")) > 3]
        print(f"📊 有效資料行: {len(data_rows)} 個")
        
        for row in data_rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) <= 3:
                    continue
                
                trend_cell = cells[1]
                count_cell = cells[2]
                time_cell = cells[3]
                
                # 提取趨勢關鍵字
                trend_text = ""
                trend_divs = trend_cell.find_elements(By.TAG_NAME, "div")
                for div in trend_divs:
                    text = div.text.strip()
                    if (text and 
                        "次搜尋" not in text and 
                        "活躍" not in text and 
                        "持續時間" not in text and 
                        "·" not in text):
                        trend_text = text
                        break
                
                # 提取搜尋量
                count_text = count_cell.text.strip()
                search_volume = ""
                count_matches = re.findall(r'(\d+[\d,]*\+)', count_text)
                for match in count_matches:
                    if re.match(r'^\d+[\d,]*\+$', match):
                        search_volume = match
                        break
                
                # 提取開始時間
                time_text = time_cell.text.strip()
                time_match = re.search(r'(\d+\s*[小時分鐘]+前)', time_text)
                started_time = time_match.group(1) if time_match else ""
                
                # 如果所有資料都齊全，加入到結果中
                if trend_text and search_volume and started_time:
                    trends.append({
                        "googleTrend": trend_text,
                        "searchVolume": search_volume,
                        "started": started_time
                    })
                    
            except Exception as e:
                print(f"⚠️ 解析行時出錯: {e}")
                continue
        
    except Exception as e:
        print(f"❌ 爬取過程中出錯: {e}")
    
    finally:
        driver.quit()
    
    return trends

def save_trends_data(trends: List[Dict[str, str]]) -> Path:
    """儲存趨勢資料到 JSON 檔案"""
    data = {
        "updated": datetime.now().isoformat() + "Z",
        "trends": trends
    }
    
    # 確保 data 資料夾存在
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # 寫入 JSON 檔案
    output_file = data_dir / "google-trends.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 資料已儲存至: {output_file}")
    return output_file


def main() -> None:
    """主函數"""
    print("🔍 Google 熱搜爬蟲 - Python 版本")
    print("=" * 50)
    
    # 爬取資料
    trends = scrape_google_trends()
    
    if trends:
        # 儲存資料
        save_trends_data(trends)
        
        # 顯示結果摘要
        print("✅ 擷取完成:", trends[:5])
        print(f"📊 總共找到 {len(trends)} 個趨勢")
    else:
        print("❌ 沒有找到任何趨勢資料")

if __name__ == "__main__":
    main()
