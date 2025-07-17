#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BBC 中文新聞爬蟲 - Python 版本
爬取 BBC 中文網 RSS 新聞資料
"""

import json
import time
import random
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_random_user_agent() -> str:
    """獲取隨機 User-Agent"""
    try:
        ua = UserAgent()
        return ua.random
    except Exception:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
    """隨機延遲"""
    delay = random.uniform(min_seconds, max_seconds)
    print(f"⏳ 隨機延遲 {delay:.2f} 秒...")
    time.sleep(delay)

def parse_rss_feed(xml_content: str) -> List[Dict[str, Any]]:
    """解析 RSS XML 內容"""
    articles = []
    
    try:
        soup = BeautifulSoup(xml_content, 'xml')
        
        # 獲取頻道資訊
        channel = soup.find('channel')
        if not channel:
            print("❌ 未找到 RSS channel")
            return []
        
        # 解析所有文章項目
        items = channel.find_all('item')
        print(f"📊 找到 {len(items)} 篇文章")
        
        for item in items:
            try:
                title_elem = item.find('title')
                link_elem = item.find('link')
                description_elem = item.find('description')
                pub_date_elem = item.find('pubDate')
                guid_elem = item.find('guid')
                
                # 提取縮圖 URL (可能在 description 的 HTML 中)
                thumbnail_url = None
                if description_elem and description_elem.get_text():
                    desc_soup = BeautifulSoup(description_elem.get_text(), 'html.parser')
                    img_tag = desc_soup.find('img')
                    if img_tag and img_tag.get('src'):
                        thumbnail_url = img_tag.get('src')
                
                article = {
                    "title": title_elem.get_text().strip() if title_elem else "",
                    "link": link_elem.get_text().strip() if link_elem else "",
                    "description": description_elem.get_text().strip() if description_elem else "",
                    "pubDate": pub_date_elem.get_text().strip() if pub_date_elem else "",
                    "guid": guid_elem.get_text().strip() if guid_elem else "",
                    "thumbnail": thumbnail_url
                }
                
                # 只添加有標題和連結的文章
                if article["title"] and article["link"]:
                    articles.append(article)
                    
            except Exception as e:
                print(f"⚠️ 解析文章時發生錯誤: {e}")
                continue
        
        print(f"✅ 成功解析 {len(articles)} 篇文章")
        return articles
        
    except Exception as e:
        print(f"❌ 解析 RSS XML 時發生錯誤: {e}")
        return []

def scrape_bbc_rss() -> Optional[List[Dict[str, Any]]]:
    """爬取 BBC 中文網 RSS 新聞"""
    rss_url = "https://feeds.bbci.co.uk/zhongwen/trad/rss.xml"
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'application/rss+xml, application/xml, text/xml',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print("🚀 開始爬取 BBC 中文網 RSS...")
        random_delay(1, 2)
        
        response = requests.get(rss_url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        print("✅ 成功獲取 RSS 內容")
        
        # 解析 RSS
        articles = parse_rss_feed(response.text)
        
        if articles:
            print(f"📰 成功爬取 {len(articles)} 篇 BBC 中文新聞")
            return articles
        else:
            print("❌ 沒有找到任何新聞文章")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP 請求錯誤: {e}")
        return None
    except Exception as e:
        print(f"❌ 爬取過程中發生錯誤: {e}")
        return None

def save_bbc_data(articles: List[Dict[str, Any]]) -> None:
    """儲存 BBC 新聞資料"""
    # 確保 data 目錄存在
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # 建立輸出資料結構
    output_data = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "source": "BBC Chinese RSS",
        "title": "BBC Chinese",
        "description": "BBC Chinese - BBC News , 中文 - 主頁",
        "link": "https://www.bbc.com/zhongwen/trad",
        "total_articles": len(articles),
        "articles": articles
    }
    
    # 儲存為 JSON
    output_path = data_dir / "bbc-trends.json"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"💾 資料已儲存至: {output_path}")
    except Exception as e:
        print(f"❌ 儲存資料時發生錯誤: {e}")

def main() -> None:
    """主函數"""
    print("📰 BBC 中文新聞爬蟲 - Python 版本")
    print("==================================================")
    
    try:
        # 爬取 BBC RSS 新聞
        articles = scrape_bbc_rss()
        
        if articles:
            # 儲存資料
            save_bbc_data(articles)
            
            # 顯示結果摘要
            print("✅ 擷取完成:")
            for i, article in enumerate(articles[:3], 1):
                print(f"  {i}. {article['title'][:60]}...")
            print(f"📊 總共找到 {len(articles)} 篇新聞")
        else:
            print("❌ 沒有找到任何新聞資料")
    
    except KeyboardInterrupt:
        print("\n⏹️ 使用者中斷執行")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 執行過程中發生錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
