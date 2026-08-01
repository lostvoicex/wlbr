"""资料更新通道路由：/api/v1/admin-data/*

仅管理员可访问，用于批量导入/导出题目、映射、学员等数据。
"""
import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.core.security import hash_password
from app.db import get_db
from app.models import KpMapping, Question, Student
from app.schemas.kp_mapping import MappingImportItem, MappingImportResult

router = APIRouter(prefix="/admin-data", tags=["admin-data"])


# ---------- 题目 ----------

@router.post(
    "/questions/import",
    response_model=dict[str, Any],
    summary="批量导入题目（JSON数组），仅管理员",
)
def import_questions(
    items: list[dict[str, Any]],
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
) -> dict[str, Any]:
    total = len(items)
    success = 0
    failed = 0
    errors: list[str] = []

    for idx, item in enumerate(items):
        try:
            # 必填字段校验
            required_fields = [
                "syllabus_version",
                "grade_level",
                "knowledge_point",
                "q_type",
                "content",
                "answer",
            ]
            for field in required_fields:
                if field not in item or item[field] is None:
                    raise ValueError(f"缺少必填字段: {field}")

            # 题型校验
            if item["q_type"] not in ("single", "judge", "coding", "program"):
                raise ValueError(f"非法题型: {item['q_type']}")

            # blocks_json 处理：如果是列表，转成 JSON 字符串
            blocks_json = item.get("blocks_json")
            if blocks_json is not None and not isinstance(blocks_json, str):
                blocks_json = json.dumps(blocks_json, ensure_ascii=False)

            # grading_rules 处理：如果是 dict/list，转成 JSON 字符串
            grading_rules = item.get("grading_rules")
            if grading_rules is not None and not isinstance(grading_rules, str):
                grading_rules = json.dumps(grading_rules, ensure_ascii=False)

            question = Question(
                syllabus_version=item["syllabus_version"],
                grade_level=int(item["grade_level"]),
                knowledge_point=item["knowledge_point"],
                q_type=item["q_type"],
                content=item["content"],
                answer=item["answer"],
                difficulty=int(item.get("difficulty", 1)),
                explanation=item.get("explanation"),
                blocks_json=blocks_json,
                grading_rules=grading_rules,
                program_lang=item.get("program_lang"),
            )
            db.add(question)
            success += 1
        except Exception as e:  # noqa: BLE001
            failed += 1
            errors.append(f"第 {idx + 1} 条: {str(e)}")

    db.commit()
    return {
        "total": total,
        "success": success,
        "failed": failed,
        "errors": errors,
    }


@router.get(
    "/questions/export",
    response_model=list[dict[str, Any]],
    summary="导出所有题目（JSON数组），仅管理员",
)
def export_questions(
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
) -> list[dict[str, Any]]:
    questions = db.query(Question).order_by(Question.id.asc()).all()
    result = []
    for q in questions:
        item = {
            "id": q.id,
            "syllabus_version": q.syllabus_version,
            "grade_level": q.grade_level,
            "knowledge_point": q.knowledge_point,
            "q_type": q.q_type,
            "content": q.content,
            "answer": q.answer,
            "difficulty": q.difficulty,
            "explanation": q.explanation,
            "blocks_json": json.loads(q.blocks_json) if q.blocks_json else None,
            "grading_rules": json.loads(q.grading_rules) if q.grading_rules else None,
            "program_lang": q.program_lang,
            "created_at": q.created_at.isoformat() if q.created_at else None,
        }
        result.append(item)
    return result


# ---------- 映射 ----------

@router.post(
    "/mappings/import",
    response_model=MappingImportResult,
    summary="批量导入映射（JSON数组），仅管理员",
)
def import_mappings(
    items: list[MappingImportItem],
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
) -> MappingImportResult:
    total = len(items)
    success = 0
    failed = 0
    errors: list[str] = []
    imported_ids: list[int] = []

    for idx, item in enumerate(items):
        try:
            mapping = KpMapping(
                syllabus_version=item.syllabus_version,
                knowledge_point=item.knowledge_point,
                courseware_name=item.courseware_name,
                chapter=item.chapter,
                page_ref=item.page_ref,
                chapter_title=item.chapter_title,
                match_score=item.match_score,
                source=item.source,
                sort_order=item.sort_order,
            )
            db.add(mapping)
            db.flush()
            imported_ids.append(mapping.id)
            success += 1
        except Exception as e:  # noqa: BLE001
            failed += 1
            errors.append(f"第 {idx + 1} 条: {str(e)}")

    db.commit()
    return MappingImportResult(
        total=total,
        success=success,
        failed=failed,
        errors=errors,
        imported_ids=imported_ids,
    )


@router.get(
    "/mappings/export",
    response_model=list[dict[str, Any]],
    summary="导出所有映射（JSON数组），仅管理员",
)
def export_mappings(
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
) -> list[dict[str, Any]]:
    mappings = db.query(KpMapping).order_by(KpMapping.id.asc()).all()
    result = []
    for m in mappings:
        item = {
            "id": m.id,
            "syllabus_version": m.syllabus_version,
            "knowledge_point": m.knowledge_point,
            "courseware_name": m.courseware_name,
            "chapter": m.chapter,
            "page_ref": m.page_ref,
            "chapter_title": m.chapter_title,
            "match_score": m.match_score,
            "source": m.source,
            "review_status": m.review_status,
            "review_level": m.review_level,
            "reviewer1_id": m.reviewer1_id,
            "reviewer2_id": m.reviewer2_id,
            "review_note": m.review_note,
            "is_active": m.is_active,
            "sort_order": m.sort_order,
            "created_at": m.created_at.isoformat() if m.created_at else None,
            "updated_at": m.updated_at.isoformat() if m.updated_at else None,
        }
        result.append(item)
    return result


# ---------- 学员 ----------

@router.post(
    "/students/import",
    response_model=dict[str, Any],
    summary="批量导入学员（JSON数组），仅管理员",
)
def import_students(
    items: list[dict[str, Any]],
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
) -> dict[str, Any]:
    total = len(items)
    success = 0
    failed = 0
    errors: list[str] = []

    for idx, item in enumerate(items):
        try:
            # 必填字段校验
            if "name" not in item or not item["name"]:
                raise ValueError("缺少必填字段: name")
            if "grade" not in item or item["grade"] is None:
                raise ValueError("缺少必填字段: grade")

            grade = int(item["grade"])
            if not (2 <= grade <= 6):
                raise ValueError(f"年级必须在 2-6 之间: {grade}")

            # 手机号唯一校验
            phone = item.get("phone")
            if phone:
                exists = db.query(Student).filter(Student.phone == phone).first()
                if exists:
                    raise ValueError(f"手机号已存在: {phone}")

            password_hash = None
            password = item.get("password")
            if password:
                password_hash = hash_password(password)

            student = Student(
                name=item["name"],
                grade=grade,
                phone=phone,
                password_hash=password_hash,
                syllabus_target=item.get("syllabus_target"),
                learning_note=item.get("learning_note"),
            )
            db.add(student)
            success += 1
        except Exception as e:  # noqa: BLE001
            failed += 1
            errors.append(f"第 {idx + 1} 条: {str(e)}")

    db.commit()
    return {
        "total": total,
        "success": success,
        "failed": failed,
        "errors": errors,
    }


@router.get(
    "/students/export",
    response_model=list[dict[str, Any]],
    summary="导出所有学员（JSON数组），仅管理员",
)
def export_students(
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
) -> list[dict[str, Any]]:
    students = db.query(Student).order_by(Student.id.asc()).all()
    result = []
    for s in students:
        item = {
            "id": s.id,
            "name": s.name,
            "grade": s.grade,
            "phone": s.phone,
            "syllabus_target": s.syllabus_target,
            "learning_note": s.learning_note,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "updated_at": s.updated_at.isoformat() if s.updated_at else None,
        }
        result.append(item)
    return result
