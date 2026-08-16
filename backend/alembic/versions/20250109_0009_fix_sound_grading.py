"""Fix sound_play grading rule to accept sound_playuntildone

Revision ID: 20250109_0009
Revises: 20250108_0008
Create Date: 2025-01-09 00:00:00.000000

"""
import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20250109_0009'
down_revision: Union[str, None] = '20250108_0008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    rows = conn.execute(
        sa.text(
            "SELECT id, grading_rules FROM questions "
            "WHERE q_type = 'program' AND program_lang = 'scratch' "
            "AND grading_rules IS NOT NULL"
        )
    ).fetchall()

    for row in rows:
        qid = row[0]
        rules_json = row[1]
        if not rules_json:
            continue
        try:
            rules = json.loads(rules_json)
        except (json.JSONDecodeError, TypeError):
            continue

        changed = False
        for rule in rules:
            if rule.get("check") == "opcode_exists":
                opcodes = rule.get("opcodes", [])
                if "sound_play" in opcodes and "sound_playuntildone" not in opcodes:
                    opcodes.append("sound_playuntildone")
                    rule["opcodes"] = opcodes
                    changed = True

        if changed:
            new_json = json.dumps(rules, ensure_ascii=False)
            conn.execute(
                sa.text("UPDATE questions SET grading_rules = :rules WHERE id = :qid"),
                {"rules": new_json, "qid": qid},
            )


def downgrade() -> None:
    pass
