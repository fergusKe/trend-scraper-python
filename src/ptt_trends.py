#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTT 熱門文章爬蟲 - Python 版本
爬取 PTT 24小時熱門文章資料
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """設定 Chrome WebDriver"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-features=VizDisplayCompositor')
    
    # 設定更真實的用戶代理
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    options.add_argument(f'--user-agent={user_agent}')
    
    # 設定視窗大小
    options.add_argument('--window-size=1920,1080')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # 移除 webdriver 痕跡
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def extract_article_info(article_element, driver) -> Optional[Dict]:
    """從文章元素中提取資訊"""
    try:
        article_data = {}
        
        # 使用多種選擇器策略來提取推文分數
        recommend_score = ""
        recommend_selectors = [
            ".e7-recommendScore",
            "[class*='recommendScore']",
            ".recommend-score"
        ]
        
        for selector in recommend_selectors:
            try:
                score_elem = article_element.find_element(By.CSS_SELECTOR, selector)
                recommend_score = score_elem.text.strip()
                if recommend_score:
                    break
            except NoSuchElementException:
                continue
        
        # 提取推文數量
        recommend_count = ""
        count_selectors = [
            "[e7description='推文:']",
            "[class*='recommendCount']",
            ".recommend-count"
        ]
        
        for selector in count_selectors:
            try:
                count_elem = article_element.find_element(By.CSS_SELECTOR, selector)
                # 找到父元素中的數字
                parent = count_elem.find_element(By.XPATH, "..")
                count_text = parent.text.strip()
                count_match = re.search(r'(\d+)', count_text)
                if count_match:
                    recommend_count = count_match.group(1)
                    break
            except NoSuchElementException:
                continue
        
        # 提取標題和連結
        title = ""
        link = ""
        title_selectors = [
            "a[href*='/bbs/']",
            ".title a",
            ".article-title a"
        ]
        
        for selector in title_selectors:
            try:
                title_elem = article_element.find_element(By.CSS_SELECTOR, selector)
                title = title_elem.text.strip()
                link = title_elem.get_attribute('href')
                if title and link:
                    # 確保連結格式正確
                    if link.startswith('/bbs/'):
                        link = link  # 保持相對路徑
                    break
            except NoSuchElementException:
                continue
        
        # 提取作者
        author = ""
        author_selectors = [
            ".author",
            "[class*='author']",
            ".article-author"
        ]
        
        for selector in author_selectors:
            try:
                author_elem = article_element.find_element(By.CSS_SELECTOR, selector)
                author = author_elem.text.strip()
                if author:
                    break
            except NoSuchElementException:
                continue
        
        # 從連結中提取看板名稱
        board = ""
        if link:
            board_match = re.search(r'/bbs/([^/]+)/', link)
            if board_match:
                board = board_match.group(1)
        
        # 提取發文時間
        publish_time = ""
        time_selectors = [
            ".publish-time",
            "[class*='publishTime']",
            ".article-time"
        ]
        
        for selector in time_selectors:
            try:
                time_elem = article_element.find_element(By.CSS_SELECTOR, selector)
                publish_time = time_elem.text.strip()
                if publish_time:
                    break
            except NoSuchElementException:
                continue
        
        # 提取圖片 URL（如果有的話）
        image_url = ""
        try:
            img_elem = article_element.find_element(By.CSS_SELECTOR, "img")
            image_url = img_elem.get_attribute('src')
        except NoSuchElementException:
            pass
        
        # 只有當基本資訊都存在時才返回資料
        if title and link:
            article_data = {
                "recommendScore": recommend_score,
                "recommendCount": recommend_count,
                "title": title,
                "link": link,
                "author": author,
                "board": board,
                "publishTime": publish_time
            }
            
            if image_url:
                article_data["imageUrl"] = image_url
            
            return article_data
        
    except Exception as e:
        print(f"⚠️ 提取文章資訊時出錯: {e}")
    
    return None

def smart_scroll(driver, target_count=20) -> None:
    """智慧滾動策略：初始不滾動保持順序，不足20篇才輕微滾動補充"""
    print("📜 檢查是否需要滾動載入更多內容...")
    
    # 先檢查當前有多少文章
    articles = driver.find_elements(By.CSS_SELECTOR, ".e7-container, [class*='container']")
    current_count = len(articles)
    print(f"📊 目前找到 {current_count} 篇文章")
    
    if current_count >= target_count:
        print("✅ 文章數量充足，無需滾動")
        return
    
    print("📜 文章數量不足，開始輕微滾動補充...")
    
    # 輕微滾動補充
    scroll_attempts = 3
    for i in range(scroll_attempts):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(2)
        
        # 檢查是否有新文章載入
        new_articles = driver.find_elements(By.CSS_SELECTOR, ".e7-container, [class*='container']")
        new_count = len(new_articles)
        
        if new_count > current_count:
            print(f"📈 滾動後增加了 {new_count - current_count} 篇文章")
            current_count = new_count
            if current_count >= target_count:
                break
        else:
            print(f"📜 第 {i+1} 次滾動未增加新內容")

def scrape_ptt_trends():
    """爬取 PTT 熱門文章"""
    driver = setup_driver()
    articles = []
    
    try:
        print("🚀 開始爬取 PTT 熱門文章...")
        
        # 前往 PTT 熱門頁面
        driver.get('https://www.pttweb.cc/hot/all/today')
        
        # 等待頁面載入
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("✅ 頁面載入完成")
        except TimeoutException:
            print("⚠️ 頁面載入超時")
        
        # 等待一段時間讓動態內容載入
        time.sleep(3)
        
        # 智慧滾動
        smart_scroll(driver, target_count=20)
        
        # 尋找文章容器
        article_selectors = [
            ".e7-container",
            "[class*='container']",
            ".article-item",
            ".hot-article"
        ]
        
        article_elements = []
        for selector in article_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    article_elements = elements
                    print(f"✅ 使用選擇器 '{selector}' 找到 {len(elements)} 個文章元素")
                    break
            except Exception as e:
                print(f"⚠️ 選擇器 '{selector}' 失敗: {e}")
                continue
        
        if not article_elements:
            print("❌ 無法找到文章元素")
            return []
        
        print(f"📊 開始解析 {len(article_elements)} 個文章...")
        
        # 解析每篇文章
        seen_titles = set()  # 用於去重
        
        for i, article_elem in enumerate(article_elements):
            try:
                article_data = extract_article_info(article_elem, driver)
                
                if article_data and article_data.get('title'):
                    # 去重檢查
                    title = article_data['title']
                    if title not in seen_titles:
                        articles.append(article_data)
                        seen_titles.add(title)
                        print(f"✅ 第 {len(articles)} 篇: {title[:50]}...")
                    else:
                        print(f"🔄 重複文章已跳過: {title[:30]}...")
                
                # 限制最多爬取30篇
                if len(articles) >= 30:
                    break
                    
            except Exception as e:
                print(f"⚠️ 解析第 {i+1} 篇文章時出錯: {e}")
                continue
    
    except Exception as e:
        print(f"❌ 爬取過程中出錯: {e}")
    
    finally:
        driver.quit()
    
    return articles

def save_ptt_data(articles):
    """儲存 PTT 資料到 JSON 檔案"""
    data = {
        "updated": datetime.now().isoformat() + "Z",
        "total_found": len(articles),
        "returned_count": len(articles),
        "articles": articles
    }
    
    # 確保 data 資料夾存在
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # 寫入 JSON 檔案
    output_file = data_dir / "ptt-trends.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 資料已儲存至: {output_file}")
    return output_file

def main():
    """主函數"""
    print("📰 PTT 熱門文章爬蟲 - Python 版本")
    print("=" * 50)
    
    # 爬取資料
    articles = scrape_ptt_trends()
    
    if articles:
        # 儲存資料
        save_ptt_data(articles)
        
        # 顯示結果摘要
        print("✅ 爬取完成!")
        print(f"📊 總共找到 {len(articles)} 篇文章")
        
        # 顯示前幾篇文章標題
        for i, article in enumerate(articles[:5], 1):
            print(f"{i}. {article.get('title', 'N/A')[:60]}...")
    else:
        print("❌ 沒有找到任何文章")

if __name__ == "__main__":
    main()
