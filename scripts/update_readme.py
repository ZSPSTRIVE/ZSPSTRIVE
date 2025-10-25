from github import Github
import os
import re
from datetime import datetime

# 获取 GitHub token
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

username = "ZSPSTRIVE"
user = g.get_user(username)

# 获取所有非 fork 的仓库，按最后推送时间排序
repos = sorted(
    [repo for repo in user.get_repos() if not repo.fork],
    key=lambda r: r.pushed_at,
    reverse=True
)

# 只取最近更新的前 6 个项目
latest_repos = repos[:6]

# 项目图标映射
project_icons = {
    'AI-tiku': '🧠',
    'CloudPix': '☁️', 
    'LangChain4j-study-java': '🧩',
    'CARDON-AI-predict': '📈',
    'profile': '👤',
    'ZSPSTRIVE': '👤'
}

# 生成项目表格 Markdown - 匹配你的风格
table = "### 🆕 最新更新项目\n\n"
table += "| 项目名 | 简介 | 技术栈 | Stars |\n"
table += "|:--------|:------|:--------|:------|\n"

for r in latest_repos:
    # 获取项目图标
    icon = project_icons.get(r.name, '🚀')
    
    # 处理描述，避免表格错位
    desc = (r.description or "暂无描述").replace("|", "｜")
    if len(desc) > 50:
        desc = desc[:47] + "..."
    
    # 获取主要语言作为技术栈
    tech_stack = r.language or "Mixed"
    
    # 格式化项目行
    table += f"| {icon} [{r.name}]({r.html_url}) | {desc} | {tech_stack} | ⭐ {r.stargazers_count} |\n"

# 添加更新时间
table += f"\n> 🕒 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)\n"

# 读取 README
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# 替换标记区域
pattern = r"(?s)(?<=<!-- PROJECTS-LIST:START -->).*?(?=<!-- PROJECTS-LIST:END -->)"
new_content = f"\n{table}\n"
updated = re.sub(pattern, new_content, readme)

# 写回 README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)

print(f"✅ 成功更新 README.md，包含 {len(latest_repos)} 个最新项目")
