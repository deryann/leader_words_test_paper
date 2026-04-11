@echo off
REM ============================================================
REM Build script: package run.py --gui as a standalone Windows exe
REM using Nuitka. Run this from the project root.
REM
REM Prerequisites:
REM   1. C compiler installed (MSVC via Visual Studio Build Tools, or MinGW64)
REM   2. Nuitka installed: uv pip install nuitka
REM
REM Output: dist\WordTestPaperGenerator.exe
REM ============================================================

echo [1/2] Building standalone folder first (easier to debug)...
.venv\Scripts\python -m nuitka ^
  --standalone ^
  --windows-disable-console ^
  --enable-plugin=tk-inter ^
  --include-data-dir=cfg-202602=cfg-202602 ^
  --include-data-dir=icons=icons ^
  --include-data-dir=static=static ^
  --include-package=PIL ^
  --include-package=docx ^
  --include-package-data=docx ^
  --nofollow-import-to=fastapi ^
  --nofollow-import-to=uvicorn ^
  --nofollow-import-to=starlette ^
  --windows-icon-from-ico=icons\score.ico ^
  --output-dir=dist ^
  run.py

if %errorlevel% neq 0 (
    echo [ERROR] Standalone build failed. Fix errors above before trying onefile build.
    pause
    exit /b 1
)

echo.
echo [DONE] Standalone build succeeded.
echo        Test it: dist\run.dist\run.exe
echo.
echo [2/2] Building single .exe (onefile)...
.venv\Scripts\python -m nuitka ^
  --onefile ^
  --windows-disable-console ^
  --enable-plugin=tk-inter ^
  --include-data-dir=cfg-202602=cfg-202602 ^
  --include-data-dir=icons=icons ^
  --include-data-dir=static=static ^
  --include-package=PIL ^
  --include-package=docx ^
  --include-package-data=docx ^
  --nofollow-import-to=fastapi ^
  --nofollow-import-to=uvicorn ^
  --nofollow-import-to=starlette ^
  --windows-icon-from-ico=icons\score.ico ^
  --output-filename=WordTestPaperGenerator.exe ^
  --output-dir=dist ^
  run.py

if %errorlevel% neq 0 (
    echo [ERROR] Onefile build failed.
    pause
    exit /b 1
)

echo.
echo [DONE] Onefile build succeeded: dist\WordTestPaperGenerator.exe
pause
