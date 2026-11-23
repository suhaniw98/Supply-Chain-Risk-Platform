
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from database.models import Base

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

lines = [
    "# Database Schema Documentation",
    "",
    "## Overview",
    "",
    "The database contains the following SQLAlchemy models:",
    ""
]

for table in Base.metadata.sorted_tables:
    lines.append(f"## Table: `{table.name}`")
    lines.append("")
    lines.append("| Column | Data Type | Primary Key | Nullable | Foreign Key |")
    lines.append("|---|---|---|---|---|")

    for column in table.columns:
        foreign_keys = [
            fk.target_fullname for fk in column.foreign_keys
        ]

        fk_text = ", ".join(foreign_keys) if foreign_keys else "No"

        lines.append(
            f"| {column.name} | {column.type} | "
            f"{'Yes' if column.primary_key else 'No'} | "
            f"{'Yes' if column.nullable else 'No'} | "
            f"{fk_text} |"
        )

    lines.append("")

lines.extend(["## Relationships", ""])

for table in Base.metadata.sorted_tables:
    for column in table.columns:
        for fk in column.foreign_keys:
            lines.append(
                f"- `{table.name}.{column.name}` references "
                f"`{fk.target_fullname}`"
            )

output_file = REPORT_DIR / "database_schema.md"
output_file.write_text("\n".join(lines), encoding="utf-8")

print("Database Schema Documentation Generated!")
print("Total Tables:", len(Base.metadata.tables))
print("Saved:", output_file)
