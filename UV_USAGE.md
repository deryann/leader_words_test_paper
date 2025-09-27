# UV 虛擬環境設定指南

本專案使用 [uv](https://github.com/astral-sh/uv) 作為 Python 套件和虛擬環境管理工具。

## 安裝 uv

### Windows (PowerShell)
```powershell
# 方法 1: 使用官方安裝腳本
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 方法 2: 使用 pip 安裝 (如果上面的方法不行)
pip install uv
```

安裝完成後，重新開啟 PowerShell 視窗。

## 專案設定

### 1. 驗證 uv 安裝
```powershell
uv --version
```

### 2. 安裝專案依賴
```powershell
# 進入專案目錄
cd d:\git_proj\leader_words_test_paper

# 只安裝運行時依賴
uv pip install python-docx fastapi uvicorn[standard] pillow

# 或者使用 sync 安裝所有依賴
uv sync --no-install-project
```

## 如果 uv sync 失敗

如果遇到 `uv sync` 錯誤，可以使用以下替代方法：

### 方法 1: 手動安裝依賴
```powershell
# 建立虛擬環境
uv venv

# 啟用虛擬環境
.\.venv\Scripts\Activate.ps1

# 安裝依賴
uv pip install python-docx fastapi uvicorn[standard] pillow
```

### 方法 2: 使用 pip 模式
```powershell
# 如果 uv 有問題，可以暫時使用傳統 pip 方式
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install python-docx fastapi uvicorn[standard] pillow
```

## 常用命令

### 套件管理
```powershell
# 安裝新套件
uv add package-name

# 安裝開發用套件
uv add --dev package-name

# 移除套件
uv remove package-name

# 更新所有套件
uv sync --upgrade

# 查看已安裝套件
uv pip list
```

### 執行應用程式
```powershell
# 使用 GUI 模式
uv run python run.py --gui

# 使用命令列模式
uv run python run.py -i 1A-P12.json

# 啟動 Web 伺服器
uv run uvicorn app:app --reload

# 使用專案定義的腳本
uv run test-paper-generator --gui
uv run test-paper-gui
```

### 開發工具
```powershell
# 執行測試
uv run pytest

# 程式碼格式化
uv run black .

# 程式碼檢查
uv run flake8 .

# 型別檢查
uv run mypy .
```

## 檔案說明

- `pyproject.toml`: 專案配置檔案，定義專案資訊、依賴套件和工具設定
- `.python-version`: 指定專案使用的 Python 版本（3.11）
- `uv.lock`: 自動生成的鎖定檔案，確保依賴版本的一致性（請勿手動編輯）

## 專案依賴

### 核心依賴
- `python-docx`: 處理 Word 文檔
- `fastapi`: Web 框架
- `uvicorn`: ASGI 伺服器
- `pillow`: 圖片處理

### 開發依賴
- `pytest`: 測試框架
- `black`: 程式碼格式化
- `flake8`: 程式碼風格檢查
- `mypy`: 靜態型別檢查

## 疑難排解

### 常見問題

1. **權限錯誤**：確保您有足夠的權限執行腳本和安裝套件
2. **Python 版本問題**：確認系統已安裝 Python 3.11 或更新版本
3. **套件衝突**：使用 `uv sync --clean` 清理並重新安裝所有依賴

### 重置環境
```powershell
# 刪除虛擬環境
Remove-Item -Recurse -Force .venv

# 重新建立環境
uv sync
```

## 部署注意事項

在生產環境部署時：
1. 使用 `uv sync --no-dev` 只安裝生產依賴
2. 確保 `uv.lock` 檔案包含在版本控制中
3. 使用 `uv export --format requirements-txt > requirements.txt` 生成相容的需求檔案

## 更多資訊

- [uv 官方文檔](https://docs.astral.sh/uv/)
- [Python 專案最佳實踐](https://packaging.python.org/en/latest/guides/)