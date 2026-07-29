"""插入 3 个真实试跑学员（幂等：按手机号判重）。

用法：`cd backend && python -m app.add_trial_students`
"""
from __future__ import annotations

from app.core.security import hash_password
from app.db import SessionLocal
from app.models import Student


TRIAL_STUDENTS = [
    {
        "name": "西瓜",
        "grade": 3,
        "phone": "17586455773",
        "syllabus_target": "scratch-l1",
        "learning_note": "Scratch 水平：很棒",
        "password": "1234",
    },
    {
        "name": "番茄",
        "grade": 4,
        "phone": "15186209705",
        "syllabus_target": "scratch-l1",
        "learning_note": "Scratch 水平：中等",
        "password": "1234",
    },
    {
        "name": "小辣椒",
        "grade": 3,
        "phone": "15599530606",
        "syllabus_target": "scratch-l1",
        "learning_note": "Scratch 水平：中等",
        "password": "1234",
    },
]


def run() -> None:
    with SessionLocal() as db:
        inserted, skipped = 0, 0
        for s in TRIAL_STUDENTS:
            exist = db.query(Student).filter(Student.phone == s["phone"]).first()
            if exist:
                skipped += 1
                print(f"[trial] 已存在 phone={s['phone']} name={exist.name}，跳过")
                continue
            db.add(
                Student(
                    name=s["name"],
                    grade=s["grade"],
                    phone=s["phone"],
                    syllabus_target=s["syllabus_target"],
                    learning_note=s["learning_note"],
                    password_hash=hash_password(s["password"]),
                )
            )
            inserted += 1
            print(f"[trial] 插入 {s['name']} phone={s['phone']} note={s['learning_note']}")
        db.commit()
        print(f"[trial] 完成：新增 {inserted} 人，跳过 {skipped} 人")


if __name__ == "__main__":
    run()
