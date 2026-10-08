"""
小学生数学题生成器
支持：加法、减法、乘法、除法、混合运算
难度：一年级(20以内)、二年级(100以内)、三年级(万以内+乘法口诀)、四年级(两位数乘除)
"""
import random
from dataclasses import dataclass
from typing import List, Literal


Difficulty = Literal["grade1", "grade2", "grade3", "grade4"]
OpType = Literal["add", "sub", "mul", "div", "mixed"]


@dataclass
class MathProblem:
    """单道数学题"""
    index: int
    expression: str
    answer: float | int
    problem_type: str
    difficulty: str

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "expression": self.expression,
            "answer": self.answer,
            "type": self.problem_type,
            "difficulty": self.difficulty,
        }


# 各难度对应的数值范围和允许的运算符
DIFFICULTY_CONFIG = {
    "grade1": {
        "label": "一年级 (20以内加减)",
        "max_num": 20,
        "ops": ["+", "-"],
        "allow_negative": False,
        "allow_decimal": False,
    },
    "grade2": {
        "label": "二年级 (100以内加减)",
        "max_num": 100,
        "ops": ["+", "-"],
        "allow_negative": False,
        "allow_decimal": False,
    },
    "grade3": {
        "label": "三年级 (万以内加减 + 乘法口诀)",
        "max_num": 10000,
        "ops": ["+", "-", "×"],
        "allow_negative": False,
        "allow_decimal": False,
    },
    "grade4": {
        "label": "四年级 (两位数乘除 + 混合)",
        "max_num": 100,
        "ops": ["+", "-", "×", "÷"],
        "allow_negative": False,
        "allow_decimal": True,
    },
}


def _gen_add(cfg: dict) -> MathProblem:
    a = random.randint(1, cfg["max_num"])
    b = random.randint(1, cfg["max_num"])
    return MathProblem(0, f"{a} + {b} =", a + b, "加法", "")


def _gen_sub(cfg: dict) -> MathProblem:
    a = random.randint(1, cfg["max_num"])
    b = random.randint(1, cfg["max_num"])
    if not cfg["allow_negative"] and a < b:
        a, b = b, a
    return MathProblem(0, f"{a} - {b} =", a - b, "减法", "")


def _gen_mul(cfg: dict) -> MathProblem:
    # 乘法控制在合理范围：二年级~三年级用乘法口诀(9×9)，四年级用两位数
    if cfg["max_num"] <= 1000:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
    else:
        a = random.randint(10, 99)
        b = random.randint(2, 9)
    return MathProblem(0, f"{a} × {b} =", a * b, "乘法", "")


def _gen_div(cfg: dict) -> MathProblem:
    # 除法保证整除
    b = random.randint(2, 9)
    quotient = random.randint(2, min(99, cfg["max_num"] // b))
    a = b * quotient
    return MathProblem(0, f"{a} ÷ {b} =", quotient, "除法", "")


def _gen_mixed(cfg: dict) -> MathProblem:
    """生成两步混合运算题"""
    op1, op2 = random.sample(cfg["ops"], 2)
    a = random.randint(2, 20)
    b = random.randint(2, 20)
    c = random.randint(2, 20)

    # 先算第一步
    if op1 == "+":
        step1 = a + b
    elif op1 == "-":
        if a < b:
            a, b = b, a
        step1 = a - b
    elif op1 == "×":
        step1 = a * b
    else:  # ÷
        b = random.randint(2, 9)
        step1 = (random.randint(2, 9) * b) // b

    # 第二步
    if op2 == "+":
        result = step1 + c
        expr = f"{a} {op1} {b} + {c} ="
    elif op2 == "-":
        if step1 < c:
            c = random.randint(1, step1)
        result = step1 - c
        expr = f"{a} {op1} {b} - {c} ="
    elif op2 == "×":
        result = step1 * c
        expr = f"({a} {op1} {b}) × {c} ="
    else:
        result = step1 // c if step1 % c == 0 else step1
        expr = f"({a} {op1} {b}) ÷ {c} ="

    return MathProblem(0, expr, result, "混合运算", "")


GENERATORS = {
    "add": _gen_add,
    "sub": _gen_sub,
    "mul": _gen_mul,
    "div": _gen_div,
    "mixed": _gen_mixed,
}


def generate_problems(
    count: int = 100,
    difficulty: Difficulty = "grade2",
    op_type: OpType = "mixed",
) -> List[MathProblem]:
    """
    生成数学题列表

    Args:
        count: 题目数量 (100~200)
        difficulty: 难度等级 grade1/grade2/grade3/grade4
        op_type: 题型 add/sub/mul/div/mixed

    Returns:
        MathProblem 列表
    """
    count = max(10, min(200, count))  # 限制 10~200
    cfg = DIFFICULTY_CONFIG.get(difficulty, DIFFICULTY_CONFIG["grade2"])
    problems: List[MathProblem] = []

    for i in range(1, count + 1):
        if op_type == "mixed":
            # 随机选一种当前难度支持的题型
            actual_op = random.choice(cfg["ops"])
            op_key = {"+": "add", "-": "sub", "×": "mul", "÷": "div"}[actual_op]
            # 三年级及以上有一定概率出混合题
            if difficulty in ("grade3", "grade4") and random.random() < 0.15:
                p = _gen_mixed(cfg)
            else:
                p = GENERATORS[op_key](cfg)
        else:
            p = GENERATORS[op_type](cfg)

        p.index = i
        p.difficulty = cfg["label"]
        problems.append(p)

    return problems


def export_as_txt(problems: List[MathProblem], path: str, with_answer: bool = False):
    """导出为纯文本试卷"""
    with open(path, "w", encoding="utf-8") as f:
        f.write("=" * 40 + "\n")
        f.write("       小学生数学口算练习\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"姓名: ____________   日期: ____________   用时: ______分钟\n\n")

        # 题目区，每题一行，两列排列
        half = (len(problems) + 1) // 2
        for i in range(half):
            left = problems[i]
            line = f"{left.index:>3}. {left.expression:<15}"
            if i + half < len(problems):
                right = problems[i + half]
                line += f"  {right.index:>3}. {right.expression}"
            f.write(line + "\n")

        if with_answer:
            f.write("\n" + "=" * 40 + "\n")
            f.write("              参考答案\n")
            f.write("=" * 40 + "\n")
            for i in range(half):
                left = problems[i]
                line = f"{left.index:>3}. {left.answer:<10}"
                if i + half < len(problems):
                    right = problems[i + half]
                    line += f"  {right.index:>3}. {right.answer}"
                f.write(line + "\n")


def export_as_csv(problems: List[MathProblem], path: str):
    """导出为 CSV (题号, 题目, 答案, 题型, 难度)"""
    import csv
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["题号", "题目", "答案", "题型", "难度"])
        for p in problems:
            writer.writerow([p.index, p.expression, p.answer, p.problem_type, p.difficulty])


if __name__ == "__main__":
    # 自测
    ps = generate_problems(count=10, difficulty="grade2")
    for p in ps:
        print(f"{p.index:>2}. {p.expression} {p.answer}")
