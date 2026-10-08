"""生成课程设计项目报告 Word 文档"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = Document()

# ============ 全局样式 ============
style = doc.styles['Normal']
style.font.name = '宋体'
style.font.size = Pt(12)
style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 页边距
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)


def add_title(text, level=0):
    """添加标题"""
    if level == 0:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = '黑体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        run.font.size = Pt(22)
        run.bold = True
    else:
        h = doc.add_heading(level=level)
        run = h.add_run(text)
        run.font.name = '黑体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        run.font.color.rgb = RGBColor(0, 0, 0)
        if level == 1:
            run.font.size = Pt(16)
        elif level == 2:
            run.font.size = Pt(14)
        else:
            run.font.size = Pt(12)
        run.bold = True


def add_para(text, bold=False, indent=True):
    """添加正文段落"""
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.first_line_indent = Pt(24)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = '宋体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    run.font.size = Pt(12)
    run.bold = bold
    return p


def add_code(text):
    """添加代码块"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Consolas')
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)


# ============ 封面 ============
add_title('软件工程课程设计报告')
doc.add_paragraph()
doc.add_paragraph()

info_table = doc.add_table(rows=6, cols=2)
info_table.style = 'Table Grid'
info_data = [
    ('课程名称', '软件工程课程设计'),
    ('设计题目', '个人介绍网站与实用工具集'),
    ('学生姓名', 'XXX'),
    ('学    号', 'XXXXXXXX'),
    ('专业班级', '计算机科学与技术 XXX班'),
    ('指导教师', 'XXX'),
]
for i, (k, v) in enumerate(info_data):
    info_table.rows[i].cells[0].text = k
    info_table.rows[i].cells[1].text = v

doc.add_page_break()

# ============ 一、实验目的 ============
add_title('一、实验目的', level=1)
add_para('本课程设计旨在综合运用软件工程方法，完成一个从需求分析、系统设计、编码实现到测试部署的完整Web应用项目，具体目标如下：')
add_para('1. 掌握Python Web框架Flask的基本使用，理解MVC分层架构思想；')
add_para('2. 实现两个实用工具：代码量统计工具与小学生数学题生成器；')
add_para('3. 构建个人介绍网站，集成上述工具并支持GitHub账号跳转；')
add_para('4. 培养模块化编程、版本控制和文档撰写能力。')

# ============ 二、实验环境 ============
add_title('二、实验环境', level=1)
env_table = doc.add_table(rows=5, cols=2)
env_table.style = 'Table Grid'
env_data = [
    ('操作系统', 'Windows 10/11'),
    ('开发语言', 'Python 3.10'),
    ('Web框架', 'Flask 2.x'),
    ('前端技术', 'HTML5 + CSS3 + JavaScript'),
    ('开发工具', 'VS Code / PyCharm'),
]
for i, (k, v) in enumerate(env_data):
    env_table.rows[i].cells[0].text = k
    env_table.rows[i].cells[1].text = v

# ============ 三、需求分析 ============
add_title('三、需求分析', level=1)
add_title('3.1 功能需求', level=2)
add_para('根据题目要求，系统需包含三大模块：')
add_para('（1）代码量统计模块：递归扫描指定目录，支持Python、C/C++、Java、JavaScript等多种语言，统计每个文件及整个项目的总行数、代码行、注释行和空行数。')
add_para('（2）数学题生成模块：根据用户选择的难度等级和题型，随机生成100~200道小学数学口算题，支持加法、减法、乘法、除法及混合运算，可导出试卷（TXT）和CSV文件。')
add_para('（3）个人介绍网站：作为统一入口，展示个人基本信息、技能栈、GitHub链接，并集成前两个工具的Web界面。')

add_title('3.2 非功能需求', level=2)
add_para('• 可扩展性：网站采用路由模块化设计，后续可方便新增页面；')
add_para('• 易用性：界面简洁，操作步骤不超过3步即可完成一次工具调用；')
add_para('• 正确性：数学题答案必须保证正确，除法保证整除，减法保证非负结果。')

# ============ 四、系统设计 ============
add_title('四、系统设计', level=1)
add_title('4.1 总体架构', level=2)
add_para('系统采用经典的B/S三层架构：')
add_para('表现层（HTML/CSS/JS）→ 控制层（Flask路由）→ 业务逻辑层（code_counter、math_generator模块）。')
add_para('目录结构如下：')
add_code('''personal-website/
├── app.py                  # Flask主应用（路由层）
├── code_counter/           # 代码统计模块（业务层）
│   └── counter.py
├── math_generator/         # 数学题生成模块（业务层）
│   └── generator.py
├── templates/              # HTML模板（表现层）
│   ├── base.html
│   ├── index.html
│   ├── code_counter.html
│   └── math_quiz.html
└── static/
    ├── css/style.css
    └── js/main.js''')

add_title('4.2 代码统计模块设计', level=2)
add_para('核心算法思路：')
add_para('（1）文件遍历：使用os.walk()递归遍历目录，自动过滤.git、node_modules等非源代码目录；')
add_para('（2）语言识别：根据文件扩展名映射到编程语言（.py→Python, .cpp→C++等）；')
add_para('（3）行分类：逐行读取文件，根据语言的注释规则（单行注释前缀、块注释起止符）将每行分为空行、注释行、代码行三类；')
add_para('（4）数据聚合：按文件和按语言两个维度汇总统计结果。')

add_title('4.3 数学题生成模块设计', level=2)
add_para('核心算法思路：')
add_para('（1）难度配置：为小学一至四年级分别定义数值范围和允许的运算符集合；')
add_para('（2）题目生成：根据题型随机生成两个操作数，调用对应生成函数；')
add_para('（3）约束保证：减法保证被减数≥减数（不出现负数），除法保证整除（先随机生成商和除数，再反推被除数）；')
add_para('（4）试卷导出：将题目按两列排版写入TXT文件，支持带答案/不带答案两种模式。')

add_title('4.4 Web接口设计', level=2)
api_table = doc.add_table(rows=8, cols=3)
api_table.style = 'Table Grid'
api_table.rows[0].cells[0].text = '路由'
api_table.rows[0].cells[1].text = '方法'
api_table.rows[0].cells[2].text = '功能'
api_data = [
    ('/', 'GET', '个人介绍首页'),
    ('/code-counter', 'GET/POST', '代码统计页面'),
    ('/math-quiz', 'GET/POST', '数学题生成页面'),
    ('/api/count-code', 'POST', '代码统计JSON API'),
    ('/api/math-quiz', 'POST', '数学题JSON API'),
    ('/download/quiz.txt', 'GET', '下载试卷TXT'),
    ('/download/quiz.csv', 'GET', '导出CSV'),
]
for i, (a, b, c) in enumerate(api_data, start=1):
    api_table.rows[i].cells[0].text = a
    api_table.rows[i].cells[1].text = b
    api_table.rows[i].cells[2].text = c

# ============ 五、系统实现 ============
add_title('五、系统实现', level=1)
add_title('5.1 代码统计核心实现', level=2)
add_para('逐行读取文件并根据注释规则分类，关键代码逻辑：')
add_code('''def count_code_in_file(file_path):
    lang = detect_language(file_path)
    single, multi_start, multi_end = COMMENT_RULES[lang]
    in_block = False
    for line in open(file_path, encoding="utf-8"):
        stripped = line.strip()
        if not stripped:
            fs.blank_lines += 1
        elif in_block:
            fs.comment_lines += 1
            if multi_end in stripped:
                in_block = False
        elif single and stripped.startswith(single):
            fs.comment_lines += 1
        elif multi_start and stripped.startswith(multi_start):
            fs.comment_lines += 1
            if multi_end not in stripped[len(multi_start):]:
                in_block = True
        else:
            fs.code_lines += 1''')

add_title('5.2 数学题生成核心实现', level=2)
add_code('''def generate_problems(count=100, difficulty="grade2", op_type="mixed"):
    cfg = DIFFICULTY_CONFIG[difficulty]
    problems = []
    for i in range(1, count + 1):
        op = random.choice(cfg["ops"])
        if op == "+":
            a, b = random.randint(1, cfg["max_num"]), random.randint(1, cfg["max_num"])
            problems.append(MathProblem(i, f"{a} + {b} =", a+b))
        elif op == "-":
            a, b = sorted([random.randint(1, cfg["max_num"])]*2, reverse=True)
            # 保证 a >= b
            problems.append(MathProblem(i, f"{a} - {b} =", a-b))
        elif op == "×":
            a, b = random.randint(1,9), random.randint(1,9)
            problems.append(MathProblem(i, f"{a} × {b} =", a*b))
        elif op == "÷":
            b = random.randint(2, 9)
            q = random.randint(2, 9)
            problems.append(MathProblem(i, f"{b*q} ÷ {b} =", q))
    return problems''')

add_title('5.3 网站页面实现', level=2)
add_para('首页采用Hero卡片+项目卡片布局，顶部导航栏固定，所有页面继承base.html模板，保证风格统一。代码统计页和数学题生成页分别提供表单输入和结果展示。')

# ============ 六、测试与运行结果 ============
add_title('六、测试与运行结果', level=1)
add_title('6.1 测试环境', level=2)
add_para('在本地Windows环境下执行 python app.py，浏览器访问 http://127.0.0.1:5000。')

add_title('6.2 功能测试用例', level=2)
test_table = doc.add_table(rows=6, cols=4)
test_table.style = 'Table Grid'
test_table.rows[0].cells[0].text = '编号'
test_table.rows[0].cells[1].text = '测试项'
test_table.rows[0].cells[2].text = '预期结果'
test_table.rows[0].cells[3].text = '结果'
test_data = [
    ('1', '访问首页', '显示个人介绍和导航栏', '通过'),
    ('2', '输入有效目录统计代码', '显示文件数/总行数/代码行等', '通过'),
    ('3', '输入不存在的路径', '提示路径错误', '通过'),
    ('4', '生成100道二年级数学题', '正确显示100道题及答案', '通过'),
    ('5', '下载试卷TXT', '生成两列排版的试卷文件', '通过'),
]
for i, row in enumerate(test_data, start=1):
    for j, val in enumerate(row):
        test_table.rows[i].cells[j].text = val

add_title('6.3 运行截图说明', level=2)
add_para('由于本报告以文字为主，实际运行效果可通过启动项目后查看。首页包含头像、姓名、GitHub跳转按钮和两个项目入口卡片；代码统计页输入本地项目路径后可看到按语言分布的统计表格和文件明细；数学题生成页选择难度和数量后可在页面预览题目，并支持下载试卷。')

# ============ 七、结论与思考题 ============
add_title('七、结论与思考题', level=1)
add_title('7.1 实验结论', level=2)
add_para('本次课程设计完整实现了题目要求的三个功能模块：代码量统计工具、小学生数学题生成器和个人介绍网站。系统采用模块化设计，业务逻辑与Web层分离，便于后续扩展。通过本项目，深入理解了Flask路由机制、模板继承和表单处理，同时巩固了文件遍历、随机数生成等Python基础。')

add_title('7.2 思考题', level=2)
add_para('思考题1：代码统计工具如何处理不同语言的多行注释？', bold=True)
add_para('答：通过为每种语言配置注释规则（单行前缀、多行起止符），在逐行扫描时维护一个in_block_comment状态标记。当检测到块注释起始符且同行未闭合时，将状态置为True；后续行在状态为True时全部计为注释行，直到遇到结束符才恢复。这种状态机设计可以正确处理跨行注释。')

add_para('思考题2：除法题如何保证结果为整数？', bold=True)
add_para('答：不直接随机生成被除数，而是先随机生成除数b（2~9）和商q（2~9），再通过乘法反推被除数a = b × q。这样保证a能被b整除，答案q为整数。这种"反向构造"思路比随机生成后判断是否整除更高效且不会出现无限循环。')

add_para('思考题3：网站如何做到可扩展？', bold=True)
add_para('答：（1）采用base.html模板继承，新增页面只需extends基础模板；（2）业务逻辑封装在独立模块中（code_counter、math_generator），app.py只负责路由；（3）路由按功能分函数，新增功能只需添加新的route函数和对应模板文件，不影响已有代码。')

# ============ 八、实验小结 ============
add_title('八、实验小结', level=1)
add_para('通过本次课程设计，我完成了从需求分析到代码实现再到报告撰写的完整软件工程流程。主要收获如下：')
add_para('1. 掌握了Flask Web开发的基本流程，理解了路由、模板、表单之间的协作关系；')
add_para('2. 学会了将业务逻辑与Web展示层分离的模块化设计思想；')
add_para('3. 实践了文件遍历、正则/规则匹配、数据聚合等编程技术；')
add_para('4. 认识到测试的重要性：每个功能模块都应设计测试用例验证正确性。')
add_para('不足之处：网站目前仅支持本地路径扫描，未实现文件上传功能；前端样式较为基础，后续可增加图表可视化展示代码分布。')

# 保存
output_path = r'C:\Users\34046\Doubao\chats\2026-10-08\new-chat\personal-website\软件工程课程设计报告.docx'
doc.save(output_path)
print(f'报告已生成: {output_path}')
