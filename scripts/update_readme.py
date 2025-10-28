# scripts/update_readme.py
from github import Github
import os
import re
from datetime import datetime, timedelta, timezone

# 获取 GitHub Token
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise RuntimeError("未检测到 GITHUB_TOKEN 环境变量，请在 workflow 中传入。")

g = Github(token)

username = "ZSPSTRIVE"
user = g.get_user(username)

# 获取所有非 fork 仓库，按最后推送时间降序排列
repos = sorted(
    [repo for repo in user.get_repos() if not repo.fork],
    key=lambda r: r.pushed_at or datetime.min,
    reverse=True
)

# 只取最近更新的前 6 个项目
latest_repos = repos[:6]

#  项目图标映射
project_icons = {
    'AI-tiku': '🧠',
    'CloudPix': '☁️',
    'LangChain4j-study-java': '🧩',
    'CARDON-AI-predict': '📈',
    'profile': '👤',
    'ZSPSTRIVE': '👤'
}

# 生成项目表格 Markdown
table = "### 🆕 最新更新项目\n\n"
table += "| 项目名 | 简介 | 技术栈 | Stars |\n"
table += "|:--------|:------|:--------|:------|\n"

for r in latest_repos:
    icon = project_icons.get(r.name, '🚀')
    desc = (r.description or "暂无描述").replace("|", "｜")
    if len(desc) > 50:
        desc = desc[:47] + "..."
    tech_stack = r.language or "Mixed"
    table += f"| {icon} [{r.name}]({r.html_url}) | {desc} | {tech_stack} | ⭐ {r.stargazers_count} |\n"

# 加上北京时间（UTC+8）
beijing_time = datetime.now(timezone.utc) + timedelta(hours=8)
table += f"\n> 🕒 最后更新: {beijing_time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)\n"

# 更新 README
readme_path = "README.md"
if not os.path.exists(readme_path):
    raise FileNotFoundError(" 未找到 README.md 文件，请确保脚本在仓库根目录执行。")

with open(readme_path, "r", encoding="utf-8") as f:
    readme = f.read()

# 确保 README 中有标记
if "<!-- PROJECTS-LIST:START -->" not in readme or "<!-- PROJECTS-LIST:END -->" not in readme:
    raise ValueError("README.md 中缺少标记 <!-- PROJECTS-LIST:START --> 或 <!-- PROJECTS-LIST:END -->")

# 用正则替换标记区域内容
pattern = r"(?s)(?<=<!-- PROJECTS-LIST:START -->).*?(?=<!-- PROJECTS-LIST:END -->)"
new_content = f"\n{table}\n"
updated = re.sub(pattern, new_content, readme)

# 写回文件
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(updated)

print(f"成功更新 README.md，包含 {len(latest_repos)} 个最新项目")
