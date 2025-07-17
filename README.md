# 🐍 Hot Now 趨勢爬蟲 - Python 版本

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![uv](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://github.com/astral-sh/uv)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

這是 [Hot Now](https://hotnow.garylin.dev) 網站的 Python 版本趨勢爬蟲，負責收集各種熱門內容的最新資訊。

## 🌟 專案簡介

Hot Now 是一個整合各大平台熱門內容的資訊聚合網站，此專案為 Python 版本的資料爬蟲，提供與 TypeScript 版本相同的功能。

-   **網站連結**: [https://hotnow.garylin.dev](https://hotnow.garylin.dev)
-   **主專案**: [https://github.com/garylin0969/hot-now](https://github.com/garylin0969/hot-now)
-   **Chrome 擴充功能**: [Hot Now ｜熱門話題一把抓](https://chromewebstore.google.com/detail/hot-now%EF%BD%9C%E7%86%B1%E9%96%80%E8%A9%B1%E9%A1%8C%E4%B8%80%E6%8A%8A%E6%8A%93/pcgkeopgenagbemoagdogljeapjhapch)

## � 支援平台

本 Python 版本爬蟲支援以下平台：

| 平台             | 內容類型     | 爬蟲頻率    | 儲存檔案                      |
| ---------------- | ------------ | ----------- | ----------------------------- |
| **PTT**          | 24H 熱門文章 | 每 10 分鐘  | `data/ptt-trends.json`        |
| **Google**       | 熱搜榜       | 每 30 分鐘  | `data/google-trends.json`     |
| **Komica(K 島)** | 熱門文章     | 每 30 分鐘  | `data/komica-trends.json`     |
| **Reddit**       | 熱門文章     | 每 30 分鐘  | `data/reddit-*-hot.json`      |
| **BBC**          | 中文新聞     | 每 30 分鐘  | `data/bbc-trends.json`        |

## 🏗️ 技術架構

### 技術棧
-   **執行環境**: Python 3.8+
-   **包管理器**: uv (現代 Python 包管理器)
-   **網頁爬蟲**: Selenium + Chrome WebDriver
-   **HTML 解析**: BeautifulSoup4 (備用)
-   **HTTP 請求**: Requests (備用)
-   **自動化**: GitHub Actions
-   **類型檢查**: mypy
-   **程式碼格式化**: black + isort

### 專案結構

```
trend-scraper-python/
├── src/                          # 爬蟲源碼
│   ├── __init__.py               # 包初始化
│   ├── main.py                   # 主程式
│   ├── google_trends.py          # Google熱搜爬蟲
│   ├── komica_trends.py          # K島熱門文章爬蟲
│   ├── ptt_trends.py             # PTT熱門文章爬蟲
│   ├── reddit_trends.py          # Reddit熱門文章爬蟲
│   └── bbc_trends.py             # BBC中文新聞爬蟲
├── data/                         # 爬蟲資料儲存
│   ├── google-trends.json        # Google熱搜資料
│   ├── komica-trends.json        # K島熱門資料
│   ├── ptt-trends.json           # PTT熱門資料
│   ├── reddit-all-hot.json       # Reddit r/all熱門資料
│   ├── reddit-taiwanese-hot.json # Reddit r/Taiwanese熱門資料
│   └── reddit-china-irl-hot.json # Reddit r/China_irl熱門資料
├── .github/workflows/            # GitHub Actions工作流程
│   ├── update-google.yml         # Google熱搜自動更新
│   ├── update-komica.yml         # K島自動更新
│   ├── update-ptt.yml            # PTT自動更新
│   └── update-reddit.yml         # Reddit自動更新
├── pyproject.toml                # 專案配置 (uv)
├── run_scraper.sh                # 執行腳本
└── README.md                     # 專案說明
```

## 🚀 快速開始

### 前置需求
-   **Python 3.8+**
-   **uv** (現代 Python 包管理器)
-   **Google Chrome** (Selenium 需要)

### 1. 安裝 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip
pip install uv
```

### 2. 安裝依賴

```bash
# 克隆或進入專案目錄
cd trend-scraper-python

# 同步依賴 (會自動建立虛擬環境)
uv sync
```

### 3. 執行爬蟲

```bash
# 使用執行腳本 (推薦)
./run_scraper.sh              # 執行所有爬蟲
./run_scraper.sh google       # 執行 Google 熱搜爬蟲
./run_scraper.sh ptt          # 執行 PTT 爬蟲
./run_scraper.sh komica       # 執行 Komica 爬蟲
./run_scraper.sh reddit       # 執行 Reddit 爬蟲
./run_scraper.sh bbc          # 執行 BBC 中文新聞爬蟲

# 或直接使用 uv
uv run python src/main.py              # 執行所有爬蟲
uv run python src/main.py google       # 執行特定爬蟲
uv run python src/google_trends.py     # 直接執行單一腳本
```

## 📦 依賴套件

| 套件                | 版本      | 用途                         |
| ------------------- | --------- | ---------------------------- |
| **selenium**        | >=4.15.2  | 瀏覽器自動化                 |
| **beautifulsoup4**  | >=4.12.2  | HTML 解析 (備用)             |
| **requests**        | >=2.31.0  | HTTP 請求 (備用)             |
| **lxml**            | >=4.9.3   | XML/HTML 解析器              |
| **fake-useragent**  | >=1.4.0   | 隨機 User-Agent 生成         |
| **webdriver-manager**| >=4.0.1  | 自動下載並管理 ChromeDriver  |

### 開發依賴

| 套件         | 版本      | 用途           |
| ------------ | --------- | -------------- |
| **black**    | >=23.0.0  | 程式碼格式化   |
| **isort**    | >=5.12.0  | import 排序    |
| **flake8**   | >=6.0.0   | 程式碼檢查     |
| **mypy**     | >=1.5.0   | 類型檢查       |
| **pytest**   | >=7.4.0   | 測試框架       |

## 🛡️ 反爬蟲策略

Python 版本採用了以下反偵測技術：

1. **隨機 User-Agent**: 模擬不同瀏覽器和設備
2. **隨機延遲**: 避免規律性存取模式  
3. **Headless 瀏覽器**: 使用 Selenium + Chrome 模擬真實瀏覽器
4. **WebDriver 痕跡移除**: 隱藏自動化瀏覽器特徵
5. **智慧重試機制**: 在失敗時自動重試
6. **穩定選擇器**: 避免依賴動態生成的 CSS 類名

## 📊 輸出格式

所有爬蟲的輸出格式保持一致，資料儲存在 `data/` 目錄：

### Google 熱搜格式
```json
{
  "updated": "2025-07-18T10:30:00.000Z",
  "trends": [
    {
      "googleTrend": "關鍵字",
      "searchVolume": "100+",
      "started": "2 小時前"
    }
  ]
}
```

### PTT 熱門文章格式
```json
{
  "updated": "2025-07-18T10:30:00.000Z",
  "total_found": 20,
  "returned_count": 20,
  "articles": [
    {
      "recommendScore": "100",
      "recommendCount": "150",
      "title": "文章標題",
      "link": "/bbs/Gossiping/M.xxx.A.xxx",
      "author": "作者",
      "board": "看板名稱",
      "publishTime": "發文時間",
      "imageUrl": "圖片網址"
    }
  ]
}
```

## 🤖 自動化部署

本專案使用 GitHub Actions 實現自動化爬蟲，每個平台都有獨立的工作流程：

| 工作流程               | 檔案                        | 執行頻率              | Cron 表達式          |
| ---------------------- | --------------------------- | --------------------- | -------------------- |
| **Google 熱搜自動更新** | `.github/workflows/update-google.yml` | 每小時第 5、35 分鐘   | `5,35 * * * *`       |
| **PTT 自動更新**       | `.github/workflows/update-ptt.yml`    | 每 10 分鐘           | `1,11,21,31,41,51 * * * *` |
| **K 島自動更新**       | `.github/workflows/update-komica.yml` | 每小時第 18、48 分鐘  | `18,48 * * * *`      |
| **Reddit 自動更新**    | `.github/workflows/update-reddit.yml` | 每小時第 28、58 分鐘  | `28,58 * * * *`      |

### 特色功能
- 使用 `uv` 進行依賴管理，速度更快
- 自動安裝 Chrome 瀏覽器
- 智慧檢測資料變更，只在有更新時才提交
- 詳細的執行日誌和錯誤報告

## 🔧 開發工具

### 程式碼品質
```bash
# 格式化程式碼
uv run black src/

# 排序 import
uv run isort src/

# 檢查程式碼風格
uv run flake8 src/

# 類型檢查
uv run mypy src/

# 執行測試
uv run pytest
```

### 建立開發環境
```bash
# 安裝包含開發依賴
uv sync --dev

# 執行所有檢查
uv run black src/ && uv run isort src/ && uv run flake8 src/ && uv run mypy src/
```

## ⚠️ 注意事項

1. **Chrome 瀏覽器**: 必須安裝 Google Chrome，Selenium 會自動下載對應的 ChromeDriver
2. **網路連線**: 需要穩定的網路連線
3. **執行時間**: 完整執行所有爬蟲大約需要 3-5 分鐘
4. **記憶體使用**: 每個瀏覽器實例約使用 100-200MB 記憶體
5. **uv 環境**: 專案使用 uv 管理依賴，確保已正確安裝 uv

## 🐛 疑難排解

### 常見問題

1. **uv 未安裝**
   ```bash
   # 安裝 uv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # 或使用 pip
   pip install uv
   ```

2. **ChromeDriver 錯誤**
   ```bash
   # uv 會自動處理依賴，如果仍有問題可手動更新
   uv sync --upgrade
   ```

3. **模組導入錯誤**
   ```bash
   # 確保在專案根目錄執行
   cd trend-scraper-python
   uv run python src/main.py
   ```

4. **權限錯誤 (Linux/macOS)**
   ```bash
   # 添加執行權限
   chmod +x run_scraper.sh
   chmod +x src/*.py
   ```

### 除錯模式

如果遇到問題，可以修改腳本中的 `headless` 設定來查看瀏覽器實際操作：

```python
# 在各個腳本的 setup_driver() 函數中
options.add_argument('--headless')  # 註解這行來顯示瀏覽器
```

### 環境重置

如果環境出現問題，可以重置：

```bash
# 清除虛擬環境
rm -rf .venv

# 重新同步
uv sync
```

## 🆚 與 TypeScript 版本的差異

| 特性           | TypeScript 版本 | Python 版本     |
| -------------- | --------------- | --------------- |
| 執行環境       | Node.js         | Python          |
| 包管理器       | pnpm            | uv              |
| 瀏覽器自動化   | Puppeteer       | Selenium        |
| 依賴管理       | package.json    | pyproject.toml  |
| 效能           | 較快            | 中等            |
| 設定複雜度     | 中等            | 簡單            |
| 除錯便利性     | 中等            | 較好            |
| 類型檢查       | 內建            | mypy            |
| 生態系統       | npm             | PyPI            |

## � 部署至 GitHub Actions

1. **Fork 專案**到您的 GitHub 帳號

2. **啟用 GitHub Actions**
   - 進入專案的 Actions 頁面
   - 點擊 "I understand my workflows, go ahead and enable them"

3. **設定工作流程權限**
   - 前往 Settings > Actions > General
   - 確保 "Workflow permissions" 設為 "Read and write permissions"

4. **手動觸發測試**
   - 前往 Actions 頁面
   - 選擇任一工作流程
   - 點擊 "Run workflow"

## 📝 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 開發流程
1. Fork 本專案
2. 建立功能分支：`git checkout -b feature/amazing-feature`
3. 提交變更：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 建立 Pull Request

### 程式碼規範
- 使用 `black` 進行程式碼格式化
- 使用 `isort` 整理 import 順序
- 使用 `mypy` 進行類型檢查
- 遵循 PEP 8 程式碼風格

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 🔗 相關連結

- **Hot Now 網站**: https://hotnow.garylin.dev
- **主專案 (TypeScript)**: https://github.com/garylin0969/trend-scraper
- **Chrome 擴充功能**: [Hot Now ｜熱門話題一把抓](https://chromewebstore.google.com/detail/hot-now%EF%BD%9C%E7%86%B1%E9%96%80%E8%A9%B1%E9%A1%8C%E4%B8%80%E6%8A%8A%E6%8A%93/pcgkeopgenagbemoagdogljeapjhapch)
- **uv 文件**: https://docs.astral.sh/uv/

---

💡 **提示**: 如果你喜歡這個專案，別忘了給個 ⭐ Star！
