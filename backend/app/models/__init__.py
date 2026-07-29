"""ORM 模型统一入口。"""
from app.models.diagnosis_session import DiagnosisSession
from app.models.kp_mapping import KpMapping
from app.models.kp_mastery_snapshot import KpMasterySnapshot
from app.models.learning_record import LearningRecord
from app.models.mapping_review import MappingReview
from app.models.oj_submission import OjSubmission
from app.models.question import Question
from app.models.student import Student
from app.models.tab_switch_event import TabSwitchEvent
from app.models.teacher import Teacher
from app.models.work_order import WorkOrder

__all__ = [
    "Student",
    "Question",
    "LearningRecord",
    "DiagnosisSession",
    "KpMasterySnapshot",
    "Teacher",
    "WorkOrder",
    "KpMapping",
    "MappingReview",
    "TabSwitchEvent",
    "OjSubmission",
]
