"""Scratch sb3 静态分析判题引擎。

.sb3 文件本质是 ZIP，内含 project.json（描述所有舞台、角色、积木、变量等）。
本引擎解析积木的 opcode，按 grading_rules 检查学生作品是否包含必要的积木结构。

判题规则格式（grading_rules 为 JSON 数组）：
[
  {"check": "opcode_exists", "opcodes": ["event_whenflagclicked"], "desc": "必须有点击绿旗积木"},
  {"check": "opcode_count", "opcode": "motion_movesteps", "min": 1, "desc": "必须有移动积木"},
  {"check": "opcode_param", "opcode": "control_repeat", "param": "TIMES", "value": "4", "desc": "重复4次"}
]

每条规则等权，全部通过 = 100 分。
"""
import base64
import io
import json
import zipfile
from typing import Any, Dict, List


def _extract_blocks_from_sb3(sb3_base64: str) -> Dict[str, Any]:
    """从 base64 编码的 sb3 文件中提取所有积木。

    Returns:
        {"targets": [{"name": "Sprite1", "blocks": {block_id: block_dict}}]}
    """
    try:
        raw = base64.b64decode(sb3_base64)
    except Exception as e:
        raise ValueError(f"sb3 base64 解码失败: {e}")

    try:
        zf = zipfile.ZipFile(io.BytesIO(raw))
    except zipfile.BadZipFile as e:
        raise ValueError(f"sb3 不是有效的 ZIP 文件: {e}")

    try:
        project_json = zf.read("project.json")
    except KeyError:
        raise ValueError("sb3 中找不到 project.json")

    try:
        project = json.loads(project_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"project.json 解析失败: {e}")

    targets = []
    for target in project.get("targets", []):
        blocks = target.get("blocks", {})
        # blocks 可能是 dict（block_id -> block dict）也可能有其他格式
        clean_blocks = {}
        for bid, block in blocks.items():
            if isinstance(block, dict):
                clean_blocks[bid] = block
        targets.append({"name": target.get("name", ""), "blocks": clean_blocks})

    return {"targets": targets}


def _get_all_opcodes(data: Dict[str, Any]) -> List[str]:
    """获取所有角色中所有积木的 opcode 列表。"""
    opcodes = []
    for target in data.get("targets", []):
        for block in target.get("blocks", {}).values():
            op = block.get("opcode")
            if op:
                opcodes.append(op)
    return opcodes


def _count_opcode(data: Dict[str, Any], opcode: str) -> int:
    """统计某个 opcode 出现的次数。"""
    count = 0
    for target in data.get("targets", []):
        for block in target.get("blocks", {}).values():
            if block.get("opcode") == opcode:
                count += 1
    return count


def _find_blocks_by_opcode(data: Dict[str, Any], opcode: str) -> List[Dict[str, Any]]:
    """查找所有指定 opcode 的积木。"""
    results = []
    for target in data.get("targets", []):
        for block in target.get("blocks", {}).values():
            if block.get("opcode") == opcode:
                results.append(block)
    return results


def _check_opcode_param(block: Dict[str, Any], param: str, value: str) -> bool:
    """检查积木的 inputs 或 fields 中某个参数是否等于指定值。

    Scratch 3.0 积木参数存储在 inputs 或 fields 中：
    - inputs: [shadow_type, [type, value]] 格式
    - fields: [[value, id]] 格式
    """
    # 检查 inputs
    inputs = block.get("inputs", {})
    if param in inputs:
        inp = inputs[param]
        if isinstance(inp, list) and len(inp) >= 2:
            val_part = inp[1]
            if isinstance(val_part, list) and len(val_part) >= 2:
                actual = str(val_part[1])
                return actual == str(value)

    # 检查 fields
    fields = block.get("fields", {})
    if param in fields:
        field = fields[param]
        if isinstance(field, list) and len(field) >= 1:
            actual = str(field[0])
            return actual == str(value)

    return False


def grade_sb3(sb3_base64: str, grading_rules_json: str) -> Dict[str, Any]:
    """对 Scratch sb3 作品进行静态分析判题。

    Args:
        sb3_base64: sb3 文件的 base64 编码
        grading_rules_json: 判题规则 JSON 字符串

    Returns:
        {
            "verdict": "accepted" | "wrong_answer" | "partial" | "compile_error",
            "score": int (0-100),
            "passed_rules": int,
            "total_rules": int,
            "details": [{"rule": ..., "passed": bool, "desc": ..., "msg": ...}],
            "stderr": None
        }
    """
    # 解析判题规则
    try:
        rules = json.loads(grading_rules_json)
    except (json.JSONDecodeError, TypeError):
        return {
            "verdict": "compile_error",
            "score": 0,
            "passed_rules": 0,
            "total_rules": 0,
            "details": [],
            "stderr": "判题规则格式错误",
        }

    if not isinstance(rules, list) or not rules:
        return {
            "verdict": "compile_error",
            "score": 0,
            "passed_rules": 0,
            "total_rules": 0,
            "details": [],
            "stderr": "判题规则为空或格式不正确",
        }

    # 解析 sb3
    try:
        data = _extract_blocks_from_sb3(sb3_base64)
    except ValueError as e:
        return {
            "verdict": "compile_error",
            "score": 0,
            "passed_rules": 0,
            "total_rules": len(rules),
            "details": [],
            "stderr": f"作品文件解析失败: {e}",
        }

    all_opcodes = _get_all_opcodes(data)
    total_rules = len(rules)
    passed_rules = 0
    details = []

    for rule in rules:
        check_type = rule.get("check", "")
        desc = rule.get("desc", "")
        passed = False
        msg = ""

        if check_type == "opcode_exists":
            # 检查是否包含指定的任意一个 opcode
            target_opcodes = rule.get("opcodes", [])
            found = [op for op in target_opcodes if op in all_opcodes]
            if found:
                passed = True
                msg = f"找到了积木: {', '.join(found)}"
            else:
                msg = f"缺少积木: {', '.join(target_opcodes)}"

        elif check_type == "opcode_count":
            # 检查某 opcode 至少出现 min 次
            opcode = rule.get("opcode", "")
            min_count = rule.get("min", 1)
            actual = _count_opcode(data, opcode)
            if actual >= min_count:
                passed = True
                msg = f"积木 {opcode} 出现了 {actual} 次（要求≥{min_count}）"
            else:
                msg = f"积木 {opcode} 只出现 {actual} 次（要求≥{min_count}）"

        elif check_type == "opcode_param":
            # 检查某 opcode 的参数值
            opcode = rule.get("opcode", "")
            param = rule.get("param", "")
            value = str(rule.get("value", ""))
            blocks = _find_blocks_by_opcode(data, opcode)
            if not blocks:
                msg = f"找不到积木 {opcode}，无法检查参数"
            else:
                for block in blocks:
                    if _check_opcode_param(block, param, value):
                        passed = True
                        msg = f"积木 {opcode} 的参数 {param}={value} 正确"
                        break
                if not passed:
                    msg = f"积木 {opcode} 的参数 {param} 不等于 {value}"

        elif check_type == "opcode_chain":
            # 检查两个 opcode 是否在同一积木链上（前后关系）
            opcode1 = rule.get("opcode1", "")
            opcode2 = rule.get("opcode2", "")
            chain_ok = _check_opcode_chain(data, opcode1, opcode2)
            if chain_ok:
                passed = True
                msg = f"{opcode1} 后面连接了 {opcode2}"
            else:
                msg = f"{opcode1} 后面没有连接 {opcode2}"

        else:
            msg = f"未知的检查类型: {check_type}"

        if passed:
            passed_rules += 1
        details.append({
            "rule": check_type,
            "passed": passed,
            "desc": desc,
            "msg": msg,
        })

    score = int((passed_rules / total_rules) * 100)
    if passed_rules == total_rules:
        verdict = "accepted"
    elif passed_rules > 0:
        verdict = "partial"
    else:
        verdict = "wrong_answer"

    return {
        "verdict": verdict,
        "score": score,
        "passed_rules": passed_rules,
        "total_rules": total_rules,
        "details": details,
        "stderr": None,
    }


def _check_opcode_chain(data: Dict[str, Any], opcode1: str, opcode2: str) -> bool:
    """检查 opcode2 是否在 opcode1 的积木链上（通过 next 指针遍历）。"""
    for target in data.get("targets", []):
        blocks = target.get("blocks", {})
        for block in blocks.values():
            if block.get("opcode") == opcode1:
                # 沿 next 指针遍历
                current = block
                while current:
                    next_id = current.get("next")
                    if next_id and next_id in blocks:
                        current = blocks[next_id]
                        if current.get("opcode") == opcode2:
                            return True
                    else:
                        break
    return False
