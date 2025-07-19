#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reddit 熱門文章爬蟲 - Python 版本
使用 Selenium 模擬瀏覽器來抓取 Reddit JSON API 資料
"""

import json
import time
import random
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

class RedditUrl:
    """Reddit URL 配置類"""
    def __init__(self, url: str, filename: str, description: str):
        self.url = url
        self.filename = filename
        self.description = description

# Reddit 子版塊配置
REDDIT_URLS = [
    RedditUrl(
        url='https://www.reddit.com/r/all/hot.json?limit=50',
        filename='data/reddit-all-hot.json',
        description='Reddit r/all 熱門文章'
    ),
    RedditUrl(
        url='https://www.reddit.com/r/Taiwanese/hot.json?limit=50',
        filename='data/reddit-taiwanese-hot.json',
        description='Reddit r/Taiwanese 熱門文章'
    ),
    RedditUrl(
        url='https://www.reddit.com/r/China_irl/hot.json?limit=50',
        filename='data/reddit-china-irl-hot.json',
        description='Reddit r/China_irl 熱門文章'
    )
]

def setup_driver():
    """設定 Chrome WebDriver"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-features=VizDisplayCompositor')
    
    # 設定隨機 User-Agent
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'--user-agent={user_agent}')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # 移除 webdriver 痕跡
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def fetch_reddit_data_with_selenium(url: str) -> Optional[Dict]:
    """使用 Selenium 獲取 Reddit JSON 資料"""
    driver = setup_driver()
    
    try:
        print(f"🔗 正在存取: {url}")
        
        # 隨機延遲避免被偵測
        delay = random.uniform(2, 5)
        print(f"⏳ 隨機延遲 {delay:.2f} 秒...")
        time.sleep(delay)
        
        # 前往 Reddit JSON API
        driver.get(url)
        
        # 等待頁面載入
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            print("⚠️ 頁面載入超時")
            return None
        
        # 額外等待確保內容完全載入
        time.sleep(2)
        
        # 獲取頁面內容
        try:
            # 先嘗試從 pre 標籤中提取 JSON
            try:
                pre_element = driver.find_element(By.TAG_NAME, "pre")
                json_text = pre_element.text
                print("✅ 從 pre 標籤中找到內容")
            except:
                # 如果沒有 pre 標籤，檢查 body 內容
                body_element = driver.find_element(By.TAG_NAME, "body")
                body_text = body_element.text
                
                # 檢查 body 內容是否看起來像 JSON
                if body_text.strip().startswith('{') and body_text.strip().endswith('}'):
                    json_text = body_text
                    print("✅ 從 body 標籤中找到 JSON 內容")
                else:
                    print("❌ 頁面內容不是 JSON 格式")
                    print(f"Content-Type: {driver.execute_script('return document.contentType')}")
                    print(f"頁面標題: {driver.title}")
                    print(f"回應內容: {body_text[:500]}...")
                    return None
            
            # 嘗試解析 JSON
            data = json.loads(json_text)
            print("✅ 成功獲取 JSON 資料")
            return data
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失敗: {e}")
            print(f"內容前500字元: {json_text[:500]}...")
            return None
            
    except Exception as e:
        print(f"❌ 獲取資料時發生錯誤: {e}")
        return None
    
    finally:
        driver.quit()

def process_reddit_data(data: Dict, description: str) -> Optional[Dict]:
    """處理 Reddit 資料"""
    try:
        if not data or 'data' not in data:
            print("❌ 無效的 Reddit 資料結構")
            return None
        
        children = data.get('data', {}).get('children', [])
        total_posts = len(children)
        
        processed_data = {
            "updated": datetime.now().isoformat() + "Z",
            "source": description,
            "total_posts": total_posts,
            "original_data": data
        }
        
        print(f"✅ 處理完成，包含 {total_posts} 篇文章")
        return processed_data
        
    except Exception as e:
        print(f"❌ 處理資料時發生錯誤: {e}")
        return None

def save_reddit_data(data: Dict, filename: str) -> Optional[Path]:
    """儲存 Reddit 資料到檔案"""
    try:
        # 確保 data 資料夾存在
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # 建立完整檔案路徑
        output_file = Path(filename)
        
        # 寫入 JSON 檔案
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 資料已儲存至: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"❌ 儲存檔案時發生錯誤: {e}")
        return None

def scrape_all_reddit_data():
    """爬取所有 Reddit 子版塊資料"""
    results = []
    
    print("🚀 開始爬取所有 Reddit 子版塊...")
    print("=" * 60)
    
    for reddit_config in REDDIT_URLS:
        print(f"\n📋 處理: {reddit_config.description}")
        print("-" * 40)
        
        try:
            # 獲取原始資料
            raw_data = fetch_reddit_data_with_selenium(reddit_config.url)
            
            if raw_data:
                # 處理資料
                processed_data = process_reddit_data(raw_data, reddit_config.description)
                
                if processed_data:
                    # 儲存資料
                    output_file = save_reddit_data(processed_data, reddit_config.filename)
                    
                    if output_file:
                        results.append({
                            'description': reddit_config.description,
                            'filename': reddit_config.filename,
                            'posts_count': processed_data.get('total_posts', 0),
                            'status': 'success'
                        })
                    else:
                        results.append({
                            'description': reddit_config.description,
                            'filename': reddit_config.filename,
                            'status': 'save_failed'
                        })
                else:
                    results.append({
                        'description': reddit_config.description,
                        'filename': reddit_config.filename,
                        'status': 'process_failed'
                    })
            else:
                results.append({
                    'description': reddit_config.description,
                    'filename': reddit_config.filename,
                    'status': 'fetch_failed'
                })
        
        except Exception as e:
            print(f"❌ 處理 {reddit_config.description} 時發生錯誤: {e}")
            results.append({
                'description': reddit_config.description,
                'filename': reddit_config.filename,
                'status': 'error',
                'error': str(e)
            })
        
        # 在子版塊之間添加延遲
        if reddit_config != REDDIT_URLS[-1]:  # 不是最後一個
            delay = random.uniform(3, 6)
            print(f"⏳ 等待 {delay:.2f} 秒後繼續下一個子版塊...")
            time.sleep(delay)
    
    return results

def main():
    """主函數"""
    print("🔥 Reddit 熱門文章爬蟲 - Python 版本")
    print("=" * 50)
    
    # 爬取所有資料
    results = scrape_all_reddit_data()
    
    # 顯示總結
    print("\n" + "=" * 60)
    print("📊 爬取結果總結:")
    print("=" * 60)
    
    success_count = 0
    total_posts = 0
    
    for result in results:
        status = result['status']
        description = result['description']
        
        if status == 'success':
            posts_count = result.get('posts_count', 0)
            print(f"✅ {description}: {posts_count} 篇文章")
            success_count += 1
            total_posts += posts_count
        else:
            print(f"❌ {description}: {status}")
            if 'error' in result:
                print(f"   錯誤: {result['error']}")
    
    print("-" * 60)
    print(f"🎯 成功爬取: {success_count}/{len(REDDIT_URLS)} 個子版塊")
    print(f"📈 總文章數: {total_posts} 篇")

if __name__ == "__main__":
    main()
