# Personal Website · 软件工程课程设计

> 四川大学 计算机科学与技术 本科生课程实验项目

## 项目简介

本项目是一个基于 **Flask** 的个人介绍网站，集成了两个实用工具模块：

| 模块 | 功能 |
|------|------|
| 📊 **代码量统计工具** | 递归扫描项目目录，支持 Python / C / C++ / Java / JavaScript / HTML / CSS / SQL / Shell / Go / Rust / PHP / Ruby 共 13 种语言，统计总行数、代码行、注释行、空行 |
| 🧮 **小学生数学题生成器** | 根据难度等级（一~四年级）和题型（加/减/乘/除/混合）随机生成 100~200 道口算题，支持导出试卷 TXT 和 CSV 文件 |
| 🌐 **个人介绍网站** | 首页展示个人信息、技能栈、GitHub 链接，集成上述两个工具的 Web 界面 |

## 技术栈

- **后端**：Python 3.10 + Flask 3.x
- **前端**：HTML5 + CSS3 + 原生 JavaScript
- **架构**：MVC 分层（路由层 / 业务逻辑层 / 模板层）

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/hblsdy/personal-website.git
cd personal-website

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 浏览器访问
# http://127.0.0.1:5000
```

## 目录结构

```
personal-website/
├── app.py                  # Flask 主应用（路由层）
├── requirements.txt
├── code_counter/           # 代码统计模块（业务逻辑层）
│   ├── __init__.py
│   └── counter.py
├── math_generator/         # 数学题生成模块（业务逻辑层）
│   ├── __init__.py
│   └── generator.py
├── templates/              # HTML 模板（表现层）
│   ├── base.html           # 基础模板（导航栏+页脚）
│   ├── index.html          # 个人介绍首页
│   ├── code_counter.html   # 代码统计页面
│   └── math_quiz.html      # 数学题生成页面
└── static/
    ├── css/style.css        # 全局样式
    └── js/main.js           # 前端脚本
```

## 功能接口

| 路由 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 个人介绍首页 |
| `/code-counter` | GET / POST | 代码统计页面 |
| `/math-quiz` | GET / POST | 数学题生成页面 |
| `/api/count-code` | POST | 代码统计 JSON API |
| `/api/math-quiz` | POST | 数学题生成 JSON API |
| `/download/quiz.txt` | GET | 下载试卷（TXT） |
| `/download/quiz.csv` | GET | 导出 CSV |

## 修改个人信息

打开 `app.py`，找到 `PROFILE` 字典：

```python
PROFILE = {
    "name": "你的名字",
    "title": "计算机科学与技术 本科生",
    "school": "四川大学",
    "github": "https://github.com/hblsdy",
    "email": "your-email@example.com",
    "bio": "...",
    "skills": ["Python", "C++", "Java", "..."],
}
```

## 作者

**王棋** — [@hblsdy](https://github.com/hblsdy)

---

⭐ 如果这个项目对你有帮助，欢迎点个 Star
