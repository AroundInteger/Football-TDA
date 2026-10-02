#!/usr/bin/env python3
"""Build Budget 02 10 26 IPA 799 v2.xlsx from IPA_799_v2_final_lock.md figures (repo archive)."""

from pathlib import Path

import openpyxl
from openpyxl.styles import Font

OUT = Path(__file__).parent / "Budget 02 10 26 IPA 799 v2.xlsx"

ROWS = [
    ("PL (RB) 0.10 FTE", "01/03/27", "29/02/28", "Salary", 8352, 6682),
    ("", "", "", "Estates", 2708, 2166),
    ("", "", "", "Inf Tech", 101, 81),
    ("", "", "", "Indirects", 6503, 5202),
    ("", "", "", "Subtotal", 17664, 14131),
    ("RA (G7 SP30) 1.0 FTE", "01/07/27", "31/12/27", "Salary", 23099, 18479),
    ("", "", "", "Estates", 13542, 10834),
    ("", "", "", "Inf Tech", 507, 406),
    ("", "", "", "Indirects", 32514, 26011),
    ("", "", "", "Subtotal", 69662, 55730),
    ("PcL (NV) 0.05 FTE", "01/03/27", "29/02/28", "Salary", 4176, 3341),
    ("", "", "", "Estates", 435, 348),
    ("", "", "", "Indirects", 3251, 2601),
    ("", "", "", "Subtotal", 7862, 6290),
]


def main() -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "IPA 799 v2"
    ws.append(["Role", "Start", "End", "Element", "100% fEC", "80% fEC"])
    for row in ROWS:
        ws.append(list(row))
    ws.append([])
    total_row = ws.max_row + 1
    ws.append(["Project total", "", "", "", 95188, 76150])
    for cell in ws[total_row]:
        cell.font = Font(bold=True)
    wb.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
