"""
个人介绍网站 + 代码统计工具 + 数学题生成器
Flask 主应用
"""
import os
import tempfile
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for

from code_counter import count_code_in_directory
from math_generator import generate_problems, export_as_txt, export_as_csv

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 上传文件最大 50MB
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "static", "uploads")

# ===================== 个人信息（请替换为你自己的）=====================
PROFILE = {
    "name": "王棋",
    "title": "计算机科学与技术 本科生",
    "school": "四川大学",
    "github": "https://github.com/hblsdy",
    "email": "508173811@qq.com",
    "bio": "热爱编程与开源，正在学习软件工程与算法设计。"
           "本站是我的课程实验作品，集成了代码统计工具和小学生数学题生成器。",
    "skills": ["Python", "C++", "Java", "数据结构与算法", "Web 开发", "操作系统"],
}
# ====================================================================


@app.route("/")
def index():
    """首页：个人介绍"""
    return render_template("index.html", profile=PROFILE)


# -------------------- 代码统计 --------------------
@app.route("/code-counter", methods=["GET", "POST"])
def code_counter_page():
    """代码统计页面"""
    result = None
    scan_path = None

    if request.method == "POST":
        scan_path = request.form.get("scan_path", "").strip()
        if scan_path and os.path.isdir(scan_path):
            stat = count_code_in_directory(scan_path)
            result = stat.to_dict()

    return render_template("code_counter.html", result=result, scan_path=scan_path, profile=PROFILE)


@app.route("/api/count-code", methods=["POST"])
def api_count_code():
    """API: 统计指定目录的代码量"""
    data = request.get_json(silent=True) or {}
    path = data.get("path", "").strip()
    if not path or not os.path.isdir(path):
        return jsonify({"error": "路径不存在或不是目录"}), 400
    stat = count_code_in_directory(path)
    return jsonify(stat.to_dict())


# -------------------- 数学题生成 --------------------
@app.route("/math-quiz", methods=["GET", "POST"])
def math_quiz_page():
    """数学题生成页面"""
    problems = []
    params = {
        "count": 100,
        "difficulty": "grade2",
        "op_type": "mixed",
    }

    if request.method == "POST":
        params["count"] = int(request.form.get("count", 100))
        params["difficulty"] = request.form.get("difficulty", "grade2")
        params["op_type"] = request.form.get("op_type", "mixed")
        problems = generate_problems(
            count=params["count"],
            difficulty=params["difficulty"],
            op_type=params["op_type"],
        )

    return render_template(
        "math_quiz.html",
        problems=problems,
        params=params,
        profile=PROFILE,
    )


@app.route("/api/math-quiz", methods=["POST"])
def api_math_quiz():
    """API: 生成数学题"""
    data = request.get_json(silent=True) or {}
    count = int(data.get("count", 100))
    difficulty = data.get("difficulty", "grade2")
    op_type = data.get("op_type", "mixed")
    show_answer = bool(data.get("show_answer", False))

    problems = generate_problems(count=count, difficulty=difficulty, op_type=op_type)
    result = [p.to_dict() for p in problems]

    if show_answer:
        return jsonify({"problems": result})
    else:
        # 不显示答案时隐藏 answer 字段
        for p in result:
            p["answer"] = "?"
        return jsonify({"problems": result})


@app.route("/download/quiz.txt")
def download_quiz_txt():
    """下载试卷 TXT"""
    count = int(request.args.get("count", 100))
    difficulty = request.args.get("difficulty", "grade2")
    op_type = request.args.get("op_type", "mixed")
    with_answer = request.args.get("with_answer", "0") == "1"

    problems = generate_problems(count=count, difficulty=difficulty, op_type=op_type)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
    export_as_txt(problems, tmp.name, with_answer=with_answer)
    return send_file(tmp.name, as_attachment=True, download_name=f"数学口算_{count}题.txt")


@app.route("/download/quiz.csv")
def download_quiz_csv():
    """下载 CSV"""
    count = int(request.args.get("count", 100))
    difficulty = request.args.get("difficulty", "grade2")
    op_type = request.args.get("op_type", "mixed")

    problems = generate_problems(count=count, difficulty=difficulty, op_type=op_type)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8-sig")
    export_as_csv(problems, tmp.name)
    return send_file(tmp.name, as_attachment=True, download_name=f"数学口算_{count}题.csv")


# -------------------- 其他页面（可扩展）--------------------
@app.route("/about")
def about():
    return render_template("index.html", profile=PROFILE)


@app.errorhandler(404)
def not_found(e):
    return render_template("index.html", profile=PROFILE), 404


if __name__ == "__main__":
    print("=" * 50)
    print("  个人介绍网站启动中...")
    print(f"  GitHub: {PROFILE['github']}")
    print("  访问 http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
