"""Wipe & re-seed questions in dev DB (safe with running FastAPI process).

只清空并重建 questions 表数据，不动 students/learning_records，避免破坏正在跑的会话。
"""
from app.db import SessionLocal
from app.models import Question
from app.seed import DEMO_QUESTIONS as QUESTIONS


def main() -> None:
    with SessionLocal() as db:
        db.query(Question).delete()
        db.commit()
        for q in QUESTIONS:
            db.add(Question(**q))
        db.commit()
        total = db.query(Question).count()
        l1 = db.query(Question).filter(Question.syllabus_version == "scratch-l1").count()
        kps = sorted({r.knowledge_point for r in db.query(Question).filter(Question.syllabus_version == "scratch-l1")})
        print(f"[reseed] total={total} l1={l1}")
        print(f"[reseed] L1 KPs: {kps}")


if __name__ == "__main__":
    main()
