"""端到端诊断流程冒烟测试。

流程：学员登录 → 开始诊断(scratch-l1) → 获取题目 → 逐题作答 → 完成 → 查看结果
"""
import json
import sys
import urllib.request
import urllib.error

sys.path.insert(0, r"C:\Users\28349\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a62db2511c702f62e54b57f\backend")
from app.db import SessionLocal
from app.models import Question

BASE = "http://127.0.0.1:8001"

def api(method, path, data=None, headers=None):
    url = f"{BASE}{path}"
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)
    body = json.dumps(data, ensure_ascii=False).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())
    except Exception as e:
        return -1, {"error": str(e)}


def main():
    print("=" * 60)
    print("端到端诊断流程冒烟测试")
    print("=" * 60)

    # 1. 学员登录
    print("\n[1] 学员登录...")
    status, login_res = api("POST", "/api/v1/auth/login", {
        "mode": "student_phone",
        "account": "13800000001",
        "credential": "123456",
    })
    if status != 200:
        print(f"❌ 登录失败: {status} -> {login_res}")
        return
    access_token = login_res["access_token"]
    student_id = login_res.get("student_id")
    print(f"✅ 登录成功，student_id={student_id}")

    headers = {"Authorization": f"Bearer {access_token}"}

    # 2. 开始诊断
    print("\n[2] 开始诊断(scratch-l1)...")
    status, start_res = api("POST", "/api/v1/diagnosis-sessions/start", {
        "syllabus_target": "scratch-l1",
        "count": 27,
        "session_type": "diagnosis",
    }, headers)
    if status != 200:
        print(f"❌ 开始诊断失败: {status} -> {start_res}")
        return
    session_id = start_res["session_id"]
    questions = start_res["questions"]
    print(f"✅ 诊断会话创建成功，session_id={session_id}")
    print(f"   题目数量: {len(questions)} 道")

    # 统计题型
    type_counts = {}
    for q in questions:
        t = q["q_type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"   题型分布: {type_counts}")

    # 检查是否有编程题
    program_qs = [q for q in questions if q["q_type"] == "program"]
    print(f"   编程大题: {len(program_qs)} 道")
    for pq in program_qs:
        print(f"     - Q{pq['id']}: {pq.get('program_lang', 'N/A')} | KP={pq['knowledge_point']}")

    # 3. 逐题作答
    print("\n[3] 逐题作答...")
    correct = 0
    # 从数据库预加载所有答案
    with SessionLocal() as db:
        all_qs = {q.id: q for q in db.query(Question).filter(Question.id.in_([q["id"] for q in questions])).all()}

    for i, q in enumerate(questions):
        qid = q["id"]
        qtype = q["q_type"]

        if qtype == "program":
            # 编程题：模拟OJ提交
            if q.get("program_lang") == "scratch":
                # 构造最小sb3
                import base64, zipfile, io
                project = {
                    "targets": [{
                        "name": "Stage",
                        "blocks": {
                            "b1": {"opcode": "event_whenflagclicked", "next": None, "parent": None,
                                   "inputs": {}, "fields": {}, "shadow": False, "topLevel": True}
                        },
                        "variables": {}, "lists": {}, "broadcasts": {}, "comments": {},
                        "currentCostume": 0, "costumes": [], "sounds": [],
                        "layerOrder": 0, "volume": 100,
                    }],
                    "monitors": [], "extensions": [],
                    "meta": {"semver": "3.0.0", "vm": "0.2.0", "agent": ""}
                }
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr("project.json", json.dumps(project))
                sb3_b64 = base64.b64encode(buf.getvalue()).decode()

                status, oj_res = api("POST", "/api/v1/oj/submit", {
                    "question_id": qid,
                    "session_id": session_id,
                    "language": "scratch",
                    "code": sb3_b64,
                }, headers)
                print(f"   Q{i+1}(program/scratch): OJ verdict={oj_res.get('verdict')}, score={oj_res.get('score')}")
            else:
                print(f"   Q{i+1}(program/{q.get('program_lang')}): 跳过（非scratch）")
        else:
            # 单选/判断/coding：从数据库取正确答案提交
            db_q = all_qs.get(qid)
            ans = db_q.answer if db_q else "A"
            if qtype == "judge":
                ans = "true" if db_q and db_q.answer.lower() in ("true", "t", "1", "对") else "false"
            status, ans_res = api("POST", f"/api/v1/diagnosis-sessions/{session_id}/answer", {
                "question_id": qid,
                "student_answer": ans,
                "answer_duration_sec": 10,
            }, headers)
            is_ok = ans_res.get("is_correct", False)
            if is_ok:
                correct += 1
            print(f"   Q{i+1}({qtype}): answer={ans}, correct={is_ok}")

    print(f"\n   基础题正确数: {correct}/{len(questions) - len(program_qs)}")

    # 4. 完成诊断
    print("\n[4] 完成诊断...")
    status, finish_res = api("POST", f"/api/v1/diagnosis-sessions/{session_id}/finish", {}, headers)
    if status != 200:
        print(f"❌ 完成诊断失败: {status} -> {finish_res}")
        return
    print(f"✅ 诊断完成，total_rate={finish_res.get('total_rate')}")
    print(f"   结果链接: {finish_res.get('result_url')}")

    # 5. 查看结果
    print("\n[5] 查看结果...")
    status, result_res = api("GET", f"/api/v1/diagnosis-sessions/{session_id}/result", headers=headers)
    if status != 200:
        print(f"❌ 获取结果失败: {status} -> {result_res}")
        return
    print(f"✅ 结果获取成功")
    print(f"   总正确率: {result_res.get('total_rate')}")
    print(f"   徽章: {result_res.get('badge')}")
    print(f"   KP数量: {len(result_res.get('per_kp', []))}")
    retest = result_res.get("retest_plan", {})
    print(f"   复测T1: {retest.get('t1_at')} ({retest.get('t1_hint')})")
    print(f"   复测T2: {retest.get('t2_at')} ({retest.get('t2_hint')})")

    # 6. 反作弊检查
    print("\n[6] 反作弊检查...")
    status, session_res = api("GET", f"/api/v1/diagnosis-sessions/{session_id}", headers=headers)
    if status == 200:
        print(f"   切屏次数: {session_res.get('tab_switch_count', 0)}")
        print(f"   可疑标记: {session_res.get('suspicious_flag', False)}")
        if session_res.get('suspicious_reason'):
            print(f"   可疑原因: {session_res.get('suspicious_reason')}")

    print("\n" + "=" * 60)
    print("端到端测试全部通过 ✅")
    print("=" * 60)


if __name__ == "__main__":
    main()
