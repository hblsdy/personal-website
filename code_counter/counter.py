"""
代码量统计模块
支持多语言源代码文件的行数统计：总行数、空行、注释行、代码行
"""
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List


# 支持的语言及对应文件扩展名
SUPPORTED_EXTENSIONS: Dict[str, List[str]] = {
    "Python": [".py", ".pyw"],
    "C": [".c", ".h"],
    "C++": [".cpp", ".cc", ".cxx", ".hpp", ".hxx", ".hh"],
    "Java": [".java"],
    "JavaScript": [".js", ".jsx", ".mjs"],
    "HTML": [".html", ".htm"],
    "CSS": [".css"],
    "SQL": [".sql"],
    "Shell": [".sh", ".bash"],
    "Go": [".go"],
    "Rust": [".rs"],
    "PHP": [".php"],
    "Ruby": [".rb"],
}

# 每种语言的注释规则: (单行注释前缀, 多行注释起始, 多行注释结束)
COMMENT_RULES: Dict[str, tuple] = {
    "Python": ("#", None, None),
    "C": ("//", "/*", "*/"),
    "C++": ("//", "/*", "*/"),
    "Java": ("//", "/*", "*/"),
    "JavaScript": ("//", "/*", "*/"),
    "HTML": (None, "<!--", "-->"),
    "CSS": (None, "/*", "*/"),
    "SQL": ("--", "/*", "*/"),
    "Shell": ("#", None, None),
    "Go": ("//", "/*", "*/"),
    "Rust": ("//", "/*", "*/"),
    "PHP": ("//", "/*", "*/"),
    "Ruby": ("#", "=begin", "=end"),
}


@dataclass
class FileStat:
    """单个文件的统计结果"""
    file_path: str
    language: str
    total_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    code_lines: int = 0

    def to_dict(self) -> dict:
        return {
            "file_path": self.file_path,
            "language": self.language,
            "total_lines": self.total_lines,
            "blank_lines": self.blank_lines,
            "comment_lines": self.comment_lines,
            "code_lines": self.code_lines,
        }


@dataclass
class ProjectStat:
    """整个项目的统计结果"""
    files: List[FileStat] = field(default_factory=list)
    total_files: int = 0
    total_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    code_lines: int = 0
    by_language: Dict[str, dict] = field(default_factory=dict)

    def add_file(self, fs: FileStat):
        self.files.append(fs)
        self.total_files += 1
        self.total_lines += fs.total_lines
        self.blank_lines += fs.blank_lines
        self.comment_lines += fs.comment_lines
        self.code_lines += fs.code_lines
        lang = fs.language
        if lang not in self.by_language:
            self.by_language[lang] = {"files": 0, "total": 0, "blank": 0, "comment": 0, "code": 0}
        self.by_language[lang]["files"] += 1
        self.by_language[lang]["total"] += fs.total_lines
        self.by_language[lang]["blank"] += fs.blank_lines
        self.by_language[lang]["comment"] += fs.comment_lines
        self.by_language[lang]["code"] += fs.code_lines

    def to_dict(self) -> dict:
        return {
            "total_files": self.total_files,
            "total_lines": self.total_lines,
            "blank_lines": self.blank_lines,
            "comment_lines": self.comment_lines,
            "code_lines": self.code_lines,
            "by_language": self.by_language,
            "files": [f.to_dict() for f in self.files],
        }


def detect_language(filename: str) -> str | None:
    """根据文件扩展名检测编程语言"""
    ext = os.path.splitext(filename)[1].lower()
    for lang, exts in SUPPORTED_EXTENSIONS.items():
        if ext in exts:
            return lang
    return None


def count_code_in_file(file_path: str) -> FileStat | None:
    """统计单个源代码文件的行数"""
    lang = detect_language(file_path)
    if lang is None:
        return None

    fs = FileStat(file_path=file_path, language=lang)
    single, multi_start, multi_end = COMMENT_RULES.get(lang, (None, None, None))

    in_block_comment = False
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for raw_line in f:
                line = raw_line.strip()
                fs.total_lines += 1

                # 空行
                if not line:
                    fs.blank_lines += 1
                    continue

                # 块注释处理
                if in_block_comment:
                    fs.comment_lines += 1
                    if multi_end and multi_end in line:
                        in_block_comment = False
                    continue

                # 单行注释
                if single and line.startswith(single):
                    fs.comment_lines += 1
                    continue

                # 块注释起始
                if multi_start and line.startswith(multi_start):
                    fs.comment_lines += 1
                    # 同行结束
                    if multi_end and multi_end in line[len(multi_start):]:
                        pass
                    else:
                        in_block_comment = True
                    continue

                # 代码行
                fs.code_lines += 1
    except Exception as e:
        fs.code_lines = -1  # 标记错误
        print(f"读取文件失败 {file_path}: {e}")

    return fs


# 排除目录
EXCLUDE_DIRS = {
    ".git", ".svn", ".hg", "__pycache__", "node_modules",
    "venv", ".venv", "env", "dist", "build", ".idea", ".vscode",
    "static/uploads",
}


def count_code_in_directory(root_dir: str) -> ProjectStat:
    """递归统计目录下所有支持的源代码文件"""
    result = ProjectStat()
    root_dir = os.path.abspath(root_dir)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 过滤排除目录
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]

        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            fs = count_code_in_file(fpath)
            if fs and fs.code_lines >= 0:
                # 显示相对路径
                fs.file_path = os.path.relpath(fpath, root_dir)
                result.add_file(fs)

    return result


if __name__ == "__main__":
    # 命令行直接运行时测试
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    stat = count_code_in_directory(target)
    print(f"扫描目录: {target}")
    print(f"文件数: {stat.total_files}")
    print(f"总行数: {stat.total_lines}")
    print(f"代码行: {stat.code_lines}")
    print(f"注释行: {stat.comment_lines}")
    print(f"空行:   {stat.blank_lines}")
    print("\n按语言统计:")
    for lang, info in stat.by_language.items():
        print(f"  {lang}: {info['files']}个文件, {info['code']}行代码")
