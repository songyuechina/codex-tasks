#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# D:/codex-tasks/cad/tools/function_analyzer.py
#版本 V1.0
"""
D:/codex-tasks/cad/tools/function_analyzer.py

纯函数工具模块（无 CLI / 无 __main__）：

目前实现（1~3）：
1) find_function_definitions: 递归扫描 root，找到 def/async def 的定义位置，返回 file + line
2) list_called_functions: 对某个函数体做 AST calls 提取，返回去重后的函数名列表（可选带详细调用点）
3) analyze_function_flow_via_api: 把函数源码 + calls 交给远程模型做“流程语义分析”，返回 JSON dict

预留（4）：extract_io_contract（暂不实现，等你跑通 3 再做）
"""

from __future__ import annotations

import os
import re
import ast
import json
from pathlib import Path
from typing import Any, Iterable
import time

# =========================================================
# 路径引导：找到 cad 根目录并加入 sys.path（保持你项目风格）
# =========================================================
import sys

_current = Path(__file__).resolve()
while _current.name != "cad":
    if _current.parent == _current:
        raise RuntimeError("找不到 cad 根目录")
    _current = _current.parent

CAD_ROOT = _current
if str(CAD_ROOT) not in sys.path:
    sys.path.insert(0, str(CAD_ROOT))


# =========================================================
# 0) 小工具
# =========================================================

def _safe_read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


def _strip_triple_fence(text: str) -> str:
    """兼容模型输出 ```json ...``` / ``` ... ```"""
    t = (text or "").strip()
    t = re.sub(r"^```json\s*", "", t, flags=re.I)
    t = re.sub(r"^```\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()


# =========================================================
# 1) 分析函数定义位置：返回脚本文件 + 行号
# =========================================================

class _DefFinder(ast.NodeVisitor):
    def __init__(self, func_name: str):
        self.func_name = func_name
        self.hits: list[dict] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name == self.func_name:
            self.hits.append({
                "function": node.name,
                "type": "def",
                "line": getattr(node, "lineno", None),
                "col": getattr(node, "col_offset", None),
            })
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if node.name == self.func_name:
            self.hits.append({
                "function": node.name,
                "type": "async def",
                "line": getattr(node, "lineno", None),
                "col": getattr(node, "col_offset", None),
            })
        self.generic_visit(node)


def find_function_definitions(
    func_name: str,
    *,
    root: str | Path = CAD_ROOT,
    exclude_dirs: Iterable[str] = ("__pycache__", ".git", ".venv", "venv"),
) -> list[dict]:
    """
    递归扫描 root 下所有 .py 文件，找 def/async def func_name 的定义位置。

    返回：
      [
        {"function": "...", "file": "...", "line": 123, "col": 0, "type": "def"},
        ...
      ]
    """
    rootp = Path(root)
    hits: list[dict] = []

    for p in rootp.rglob("*.py"):
        if any(part in exclude_dirs for part in p.parts):
            continue
        try:
            src = _safe_read_text(p)
            tree = ast.parse(src, filename=str(p))
            finder = _DefFinder(func_name)
            finder.visit(tree)
            for h in finder.hits:
                item = dict(h)
                item["file"] = str(p)
                hits.append(item)
        except Exception:
            continue

    hits.sort(key=lambda x: (x.get("file", ""), x.get("line") or 0))
    return hits


# =========================================================
# 2) 分析函数引用的其余函数：返回函数名列表（calls）
# =========================================================

class _CallCollector(ast.NodeVisitor):
    def __init__(self):
        self.items: list[dict] = []

    def _name_of(self, node: ast.AST) -> str:
        # foo()
        if isinstance(node, ast.Name):
            return node.id
        # a.b()
        if isinstance(node, ast.Attribute):
            left = self._name_of(node.value)
            return f"{left}.{node.attr}" if left else node.attr
        return ""

    def visit_Call(self, node: ast.Call):
        name = self._name_of(node.func)
        if name:
            self.items.append({
                "name": name,
                "line": getattr(node, "lineno", None),
                "col": getattr(node, "col_offset", None),
            })
        self.generic_visit(node)

    # 不进入子作用域，避免把内部 def/class 的调用混入
    def visit_FunctionDef(self, node: ast.FunctionDef):  # noqa: N802
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):  # noqa: N802
        return

    def visit_ClassDef(self, node: ast.ClassDef):  # noqa: N802
        return


def list_called_functions(
    file: str | Path,
    *,
    func_name: str,
    unique: bool = True,
    with_locations: bool = False,
) -> list[Any]:
    """
    在指定 file 中，找到 func_name 的 def，然后抽取该函数体内的 Call()。

    - unique=True：去重（保持出现顺序）
    - with_locations=False：返回 ["a.b", "foo", ...]
      with_locations=True：返回 [{"name":"foo","line":..,"col":..}, ...]

    注意：这里只做“语法层调用点”，不会做跨文件解析、也不会解析动态调用。
    """
    p = Path(file)
    if not p.exists():
        return []

    try:
        src = _safe_read_text(p)
        tree = ast.parse(src, filename=str(p))
    except Exception:
        return []

    target: ast.AST | None = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
            target = node
            break
    if target is None:
        return []

    collector = _CallCollector()
    # 只遍历函数体 top-level 语句
    for stmt in getattr(target, "body", []):
        collector.visit(stmt)

    if with_locations:
        items = collector.items
        if not unique:
            return items
        seen = set()
        out = []
        for it in items:
            n = it.get("name")
            if not n or n in seen:
                continue
            seen.add(n)
            out.append(it)
        return out

    # names only
    names = [it["name"] for it in collector.items if it.get("name")]
    if not unique:
        return names
    seen = set()
    out = []
    for n in names:
        if n in seen:
            continue
        seen.add(n)
        out.append(n)
    return out


# =========================================================
# 2.5) （可选）按 def 行提取函数源码（给第 3 步用）
# =========================================================

def extract_function_source(
    file: str | Path,
    *,
    def_line_1based: int,
) -> dict:
    """
    提取完整函数源码：
    - 支持超长多行参数列表
    - 正确识别 def(...): 结束位置
    """
    p = Path(file)
    if not p.exists():
        return {"ok": False, "file": str(p), "errors": ["file not found"]}

    lines = _safe_read_text(p).splitlines(True)
    i = max(0, int(def_line_1based) - 1)
    if i >= len(lines):
        return {"ok": False, "file": str(p), "errors": ["line out of range"]}

    # ---------- 1) 回溯装饰器 ----------
    start = i
    while start > 0 and lines[start - 1].lstrip().startswith("@"):
        start -= 1

    # ---------- 2) 吃完整函数签名（直到括号闭合 + 冒号） ----------
    sig_end = None
    paren = 0
    for idx in range(start, len(lines)):
        line = lines[idx]
        paren += line.count("(")
        paren -= line.count(")")
        if paren == 0 and line.rstrip().endswith(":"):
            sig_end = idx
            break

    if sig_end is None:
        return {
            "ok": False,
            "file": str(p),
            "errors": ["cannot find end of function signature"],
        }

    def_indent = len(lines[start]) - len(lines[start].lstrip(" \t"))

    # ---------- 3) 提取函数体 ----------
    end = sig_end + 1
    while end < len(lines):
        line = lines[end]
        stripped = line.strip()

        if stripped == "" or stripped.startswith("#"):
            end += 1
            continue

        indent = len(line) - len(line.lstrip(" \t"))

        # 同级 def / class → 函数结束
        if indent <= def_indent and re.match(r"^\s*(def|async\s+def|class)\s+\w+", line):
            break

        # 顶格新语句（工程近似）
        if indent <= def_indent and not line.startswith((" ", "\t")):
            break

        end += 1

    src = "".join(lines[start:end]).rstrip() + "\n"
    return {
        "ok": True,
        "file": str(p),
        "start_line": start + 1,
        "end_line": end,
        "source": src,
        "errors": [],
    }
# =========================================================
# 3) 分析函数的功能流程（远程模型 JSON）
# =========================================================


def _build_function_flow_prompt(
    *,
    func_name: str,
    func_source: str,
    local_calls: list[str] | list[dict] | None,
) -> str:
    calls_text = json.dumps(local_calls or [], ensure_ascii=False, indent=2)

    schema = {
        "function": func_name,
        "summary": "string",
        "inputs": [{"name": "string", "type": "string", "meaning": "string", "default": "string"}],
        "steps": ["string"],
        "branches": [{"when": "string", "does": "string", "returns": "string"}],
        "errors": [{"case": "string", "symptom": "string", "handling": "string", "returns": "string"}],
        "side_effects": ["string"],
        "returns": {"shape": "string", "fields": [{"path": "string", "meaning": "string", "example": "string"}]},
        "examples": [{"call": "string", "expect": "string"}],
    }

    parts = [
        # 关键：强制约束
        "你必须只输出一个 JSON 对象，不允许输出任何解释文字、前缀、后缀、markdown、代码块。",
        "如果你无法完成分析，也必须输出 JSON：",
        '{"function":"%s","summary":"","inputs":[],"steps":[],"branches":[],"errors":[{"case":"format_error","symptom":"cannot follow output contract","handling":"output the minimal json only","returns":""}],"side_effects":[],"returns":{"shape":"","fields":[]},"examples":[]}'
        % func_name,
        "",
        "输出 JSON 必须匹配如下字段结构（允许留空，但字段必须存在）：",
        _json_dumps(schema),
        "",
        "本地AST提取到的调用点：",
        calls_text,
        "",
        "函数源码（你不需要定位仓库文件，你只分析下面给出的源码）：",
        func_source.rstrip(),
    ]
    return "\n".join(parts)



def parse_sse_response_text(sse_text: str) -> dict:
    """
    把 SSE 文本按 event/data 拆出来，返回：
      { "events": [...], "last_response_obj": dict|None }
    """
    events: list[dict] = []
    last_response: dict | None = None

    event: str | None = None
    data_buf: list[str] = []

    def flush():
        nonlocal event, data_buf, last_response
        if event is None and not data_buf:
            return
        raw = "\n".join(data_buf).strip()
        item: dict[str, Any] = {"event": event, "data_raw": raw}
        try:
            if raw.startswith("{") and raw.endswith("}"):
                item["data_json"] = json.loads(raw)
        except Exception:
            pass
        events.append(item)

        dj = item.get("data_json")
        if isinstance(dj, dict) and dj.get("type") == "response.completed":
            last_response = dj.get("response")

        event = None
        data_buf = []

    for line in (sse_text or "").splitlines():
        line = line.rstrip("\n")
        if line.startswith("event:"):
            flush()
            event = line.split(":", 1)[1].strip()
        elif line.startswith("data:"):
            data_buf.append(line.split(":", 1)[1].strip())
        elif line.strip() == "":
            flush()

    flush()
    return {"events": events, "last_response_obj": last_response}


def extract_output_text_from_response(resp_obj: dict | None) -> str:
    """
    从 response 对象里提取最终输出文本。
    """
    if not isinstance(resp_obj, dict):
        return ""
    out: list[str] = []
    output = resp_obj.get("output") or []
    if not isinstance(output, list):
        return ""
    for item in output:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "message":
            content = item.get("content") or []
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "output_text":
                        out.append(c.get("text") or "")
    return "\n".join([x for x in out if x])


def fox_responses_request_sse(
    *,
    base_url: str,
    api_key: str,
    model: str,
    text: str,
    timeout: int = 60,
) -> dict:
    """
    最小通用 SSE 请求（你已验证的那套）：
    - POST {base_url}/responses
    - stream=True
    - input 必须是 list，里面是 message + input_text
    """
    import requests

    endpoint = base_url.rstrip("/") + "/responses"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "stream": True,
        "input": [
            {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": text}],
            }
        ],
    }

    r = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
    raw = r.text or ""

    if r.status_code >= 400:
        return {
            "ok": False,
            "status_code": r.status_code,
            "endpoint": endpoint,
            "error": f"HTTP {r.status_code}",
            "raw_sse_text": raw,
            "output_text": "",
            "response_id": None,
            "response_obj": None,
        }

    parsed = parse_sse_response_text(raw)
    resp_obj = parsed.get("last_response_obj")
    output_text = extract_output_text_from_response(resp_obj)

    return {
        "ok": True,
        "status_code": r.status_code,
        "endpoint": endpoint,
        "error": None,
        "raw_sse_text": raw,
        "output_text": output_text,
        "response_id": (resp_obj or {}).get("id"),
        "response_obj": resp_obj,
    }


def analyze_function_flow_via_api(
    *,
    func_name: str,
    func_source: str,
    local_calls: list[str] | list[dict] | None,
    base_url: str,
    api_key: str,
    model: str = "gpt-5.2-codex",
    timeout: int = 180,
) -> dict:
    """
    第 3 步：语义流程分析（远程模型）

    返回稳定结构：
    {
      ok: bool,
      status_code,
      endpoint,
      response_id,
      error,
      output_text,
      analysis: dict|None,   # 解析出来的 JSON
    }
    """
    prompt = _build_function_flow_prompt(
        func_name=func_name,
        func_source=func_source,
        local_calls=local_calls,
    )

    res = fox_responses_request_sse(
        base_url=base_url,
        api_key=api_key,
        model=model,
        text=prompt,
        timeout=timeout,
    )

    ret = {
        "ok": False,
        "status_code": res.get("status_code"),
        "endpoint": res.get("endpoint"),
        "response_id": res.get("response_id"),
        "error": res.get("error"),
        "output_text": res.get("output_text") or "",
        "analysis": None,
    }

    if not res.get("ok"):
        return ret

    text = (ret["output_text"] or "").strip()
    if not text:
        ret["error"] = "API返回为空 output_text"
        return ret

    try:
        cleaned = _strip_triple_fence(text)
        ret["analysis"] = json.loads(cleaned)
        ret["ok"] = True
        ret["error"] = None
    except Exception as e:
        ret["error"] = f"JSON解析失败: {e}"

    return ret

def analyze_function_flow_with_retry(
    *,
    func_name: str,
    func_source: str,
    local_calls: list[str] | list[dict] | None,
    base_url: str,
    api_key: str,
    model: str = "gpt-5.2-codex",
    timeout: int = 180,
    max_retries: int = 5,
    retry_sleep: float = 2.0,
    verbose: bool = True,   # 是否打印人类可读结果
) -> dict:
    """
    带重试的函数流程分析（推荐对外接口）

    返回给智能体的稳定结构：
    {
      ok: bool,
      retries: int,
      error: str|None,
      analysis: dict|None,
      printed: bool,   # ⭐ 新增：是否已打印人类可读结果
      raw: dict
    }
    """
    last_error = None
    last_raw = None

    for attempt in range(1, max_retries + 1):
        api_ret = analyze_function_flow_via_api(
            func_name=func_name,
            func_source=func_source,
            local_calls=local_calls,
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout=timeout,
        )

        last_raw = api_ret

        if api_ret.get("ok") and isinstance(api_ret.get("analysis"), dict):
            analysis = api_ret["analysis"]

            printed = False
            if verbose:
                print_human_flow_summary(
                    func_name=func_name,
                    analysis=analysis,
                )
                printed = True

            return {
                "ok": True,
                "retries": attempt,
                "error": None,
                "analysis": analysis,
                "printed": printed,   # ⭐
                "raw": api_ret,
            }

        last_error = api_ret.get("error") or "unknown error"

        if attempt < max_retries:
            time.sleep(retry_sleep * attempt)

    return {
        "ok": False,
        "retries": max_retries,
        "error": last_error,
        "analysis": None,
        "printed": False,   # ⭐
        "raw": last_raw,
    }


def print_human_flow_summary(
    *,
    func_name: str,
    analysis: dict,
    stream=print,   # ⭐ 新增：输出函数
):
    """
    在控制台/日志/GUI中打印“符合人类思维”的函数流程说明
    stream: 一个接收字符串的可调用对象（默认 print）
    """
    def out(msg=""):
        stream(msg)

    out("\n" + "=" * 88)
    out(f"🧠 函数流程分析：{func_name}")
    out("=" * 88)

    summary = analysis.get("summary")
    if summary:
        out("\n【总体功能】")
        out(f"  {summary}")

    inputs = analysis.get("inputs") or []
    if inputs:
        out("\n【输入参数】")
        for p in inputs:
            out(
                f" - {p.get('name')}: {p.get('meaning')} "
                f"(默认={p.get('default')})"
            )

    steps = analysis.get("steps") or []
    if steps:
        out("\n【主要执行流程】")
        for i, step in enumerate(steps, 1):
            out(f" {i}. {step}")

    branches = analysis.get("branches") or []
    if branches:
        out("\n【关键分支】")
        for b in branches:
            out(f" - 当 {b.get('when')} 时：")
            out(f"   → 执行：{b.get('does')}")
            out(f"   → 返回：{b.get('returns')}")

    errors = analysis.get("errors") or []
    if errors:
        out("\n【异常与失败路径】")
        for e in errors:
            out(f" - 情况：{e.get('case')}")
            out(f"   表现：{e.get('symptom')}")
            out(f"   处理：{e.get('handling')}")
            out(f"   返回：{e.get('returns')}")

    returns = analysis.get("returns") or {}
    if returns:
        out("\n【返回值】")
        out(f"  形式： {returns.get('shape')}")
        for f in returns.get("fields", []):
            out(
                f"   - {f.get('meaning')} "
                f"(示例：{f.get('example')})"
            )

    out("\n" + "=" * 88 + "\n")


# =========================================================
# 4) （预留）提取 I/O 合同：输入参数 + 分支输出参数
#     暂时不实现：等你跑通第三步的稳定输出再做
# =========================================================

def extract_io_contract(*args, **kwargs) -> dict:
    """
    预留：从第 3 步 analysis 里提取 “输入参数 + 多分支输出参数” 的结构化合同。
    TODO: 等你跑通第三步后再实现。
    """
    raise NotImplementedError("extract_io_contract 暂未实现：请先跑通 analyze_function_flow_via_api")




#&&% 构建函数调用合同（Build Function Call Contract）

def build_function_contract_v1(analysis: dict) -> dict:
    """
    第4步 · 第一版（完整版）
    一次性完成：
      - required / optional inputs
      - success / failure outputs
      - side effects
      - safe usage notes

    规则驱动、稳定、不引入模型
    """

    if not isinstance(analysis, dict):
        raise ValueError("analysis must be a dict")

    func_name = analysis.get("function", "")

    # =================================================
    # 1) INPUTS
    # =================================================
    required_inputs = []          # 第一版：保守策略，留空
    optional_inputs = {}

    for inp in analysis.get("inputs", []):
        name = inp.get("name")
        if not name:
            continue

        optional_inputs[name] = {
            "type": inp.get("type"),
            "meaning": inp.get("meaning"),
            "default": inp.get("default"),
        }

    # =================================================
    # 2) OUTPUTS
    # =================================================
    returns = analysis.get("returns", {}) or {}

    success_output = {
        "type": returns.get("shape"),
        "fields": returns.get("fields", []),
        "meaning": "函数正常执行时的返回结果",
    }

    failure_outputs = []
    for e in analysis.get("errors", []):
        failure_outputs.append({
            "when": e.get("case"),
            "returns": e.get("returns"),
            "meaning": e.get("symptom"),
        })

    # =================================================
    # 3) SIDE EFFECTS（关键词规则）
    # =================================================
    SIDE_EFFECT_KEYWORDS = [
        "创建", "删除", "写入", "生成",
        "打开", "关闭", "切换", "设置",
        "打印", "保存"
    ]

    side_effects = []
    for step in analysis.get("steps", []):
        for kw in SIDE_EFFECT_KEYWORDS:
            if kw in step:
                side_effects.append(step)
                break

    # 去重（保持顺序）
    seen = set()
    side_effects = [
        s for s in side_effects
        if not (s in seen or seen.add(s))
    ]

    # =================================================
    # 4) SAFE USAGE NOTES（全部有依据）
    # =================================================
    safe_usage_notes = []

    # 4.1 错误处理方式
    for e in analysis.get("errors", []):
        safe_usage_notes.append(
            f"当发生 {e.get('case')} 时，函数不会抛异常，而是返回错误字符串"
        )

    # 4.2 返回值约定
    if returns.get("shape") == "string":
        safe_usage_notes.append(
            "返回值为字符串，调用方需要通过内容判断成功或失败（例如是否以 ❌ 开头）"
        )

    # 4.3 None 语义
    for inp in analysis.get("inputs", []):
        if inp.get("default") in (None, "None"):
            safe_usage_notes.append(
                f"参数 {inp.get('name')} 为 None 时表示使用当前上下文或默认环境"
            )

    # 去重
    safe_usage_notes = list(dict.fromkeys(safe_usage_notes))

    # =================================================
    # 5) CONTRACT
    # =================================================
    contract = {
        "function": func_name,

        "inputs": {
            "required": required_inputs,
            "optional": optional_inputs,
        },

        "outputs": {
            "success": success_output,
            "failure": failure_outputs,
        },

        "side_effects": side_effects,
        "safe_usage_notes": safe_usage_notes,
    }

    return contract


















