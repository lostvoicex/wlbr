"""一次性回填 questions.blocks_json：把 coding 题的 answer 按 → 拆成积木数组。

用法：`python -m app.scripts.backfill_question_blocks`
幂等：已有 blocks_json 的题不重写。
"""
from __future__ import annotations

import json

from app.db import SessionLocal
from app.models.question import Question


def _split_answer(answer: str) -> list[str]:
    parts = [p.strip() for p in answer.split("→") if p.strip()]
    return parts


def main() -> None:
    db = SessionLocal()
    try:
        coding_qs = (
            db.query(Question)
            .filter(Question.q_type == "coding")
            .order_by(Question.id.asc())
            .all()
        )
        updated = 0
        for q in coding_qs:
            if q.blocks_json:
                print(f"skip #{q.id}: 已有 blocks_json")
                continue
            blocks = _split_answer(q.answer)
            if not blocks:
                print(f"warn #{q.id}: answer 拆分为空，跳过（answer={q.answer!r}）")
                continue
            q.blocks_json = json.dumps(blocks, ensure_ascii=False)
            updated += 1
            print(f"ok  #{q.id}: {q.blocks_json}")
        db.commit()
        print(f"---\n共处理 {len(coding_qs)} 道 coding 题，写入 {updated} 道 blocks_json")
    finally:
        db.close()


if __name__ == "__main__":
    main()
