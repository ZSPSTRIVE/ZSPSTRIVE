@echo off
echo 🚀 开始部署 GitHub Actions 自动更新工作流...

echo.
echo 📁 检查文件结构...
if not exist ".github\workflows" (
    echo ❌ .github\workflows 目录不存在
    pause
    exit /b 1
)

if not exist "scripts" (
    echo ❌ scripts 目录不存在  
    pause
    exit /b 1
)

echo ✅ 文件结构检查完成

echo.
echo 📤 开始提交到 GitHub...

git add .
git commit -m "🪄 feat: 添加自动更新 README 的 GitHub Actions 工作流

- 新增 .github/workflows/update-readme.yml 工作流配置
- 新增 scripts/update_readme.py 自动更新脚本  
- 支持每周一自动更新最新项目列表
- 支持手动触发和推送时触发
- 匹配个人主页风格，包含项目图标和技术栈信息"

echo.
echo 🔄 推送到远程仓库...
git push origin main

echo.
echo ✅ 部署完成！
echo.
echo 📋 接下来你可以：
echo 1. 访问 https://github.com/ZSPSTRIVE/ZSPSTRIVE/actions
echo 2. 找到 "🪄 Auto Update README with Latest Projects" 工作流
echo 3. 点击 "Run workflow" 手动测试
echo.
pause
