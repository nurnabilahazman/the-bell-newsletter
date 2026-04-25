#!/usr/bin/env python3
"""
Logs each Bell newsletter edition to Google Sheets.
Sets up headers, Bell branding, checkboxes, and column widths on first run.
Adds one row per edition with alternating row colours.
Usage: python tools/log_to_sheets.py
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS_PATH = Path("credentials.json")
CURRICULUM_PATH  = Path("config/curriculum.json")
SAAS_PATH        = Path("config/saas_progress.json")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

HEADERS = [
    "Week #", "Date Sent", "Deadline (Sat)", "✓ Sent",
    "Project (S1)", "Skill Learned", "✓ Built",
    "Productivity Product", "Language Product", "Children Product", "✓ Products Created",
    "SaaS Task", "✓ SaaS Done",
    "Notes"
]

# 0-based column indices that should be checkboxes
CHECKBOX_COLS = [3, 6, 10, 12]

# Bell brand colours as RGB fractions (0-1)
NAVY       = {"red": 0.102, "green": 0.102, "blue": 0.180}
GOLD       = {"red": 0.788, "green": 0.659, "blue": 0.298}
LIGHT_GREY = {"red": 0.957, "green": 0.957, "blue": 0.957}
WHITE      = {"red": 1.0,   "green": 1.0,   "blue": 1.0}


# ── helpers ────────────────────────────────────────────────────────────────────

def get_client() -> gspread.Client:
    creds = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=SCOPES)
    return gspread.authorize(creds)


def next_saturday() -> str:
    today = datetime.now()
    days_ahead = (5 - today.weekday()) % 7
    saturday = today if days_ahead == 0 else today + timedelta(days=days_ahead)
    return saturday.strftime("%Y-%m-%d")


def get_curriculum_info() -> tuple[int, str, str]:
    if not CURRICULUM_PATH.exists():
        return 1, "", ""
    with open(CURRICULUM_PATH) as f:
        data = json.load(f)
    week_num = data.get("current_week", 1)
    project  = next((p for p in data.get("projects", []) if p["week"] == week_num), {})
    title    = project.get("title", "")
    skill    = project.get("skill", "").split("—")[0].strip()
    return week_num, title, skill


def get_saas_task() -> str:
    if not SAAS_PATH.exists():
        return ""
    with open(SAAS_PATH) as f:
        data = json.load(f)
    week_num   = data.get("current_week", 1)
    milestones = data.get("milestones", [])
    current    = next((m for m in milestones if m["week"] == week_num), {})
    return current.get("task", "")


# ── first-run sheet setup ───────────────────────────────────────────────────────

def setup_sheet(spreadsheet: gspread.Spreadsheet, ws: gspread.Worksheet):
    sid = ws.id

    # Write headers
    ws.update(values=[HEADERS], range_name="A1")

    # Navy background, gold bold text on header row
    ws.format(f"A1:{chr(64 + len(HEADERS))}1", {
        "backgroundColor": NAVY,
        "textFormat": {
            "bold": True,
            "foregroundColor": GOLD,
            "fontSize": 10
        },
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    })

    # Column widths (pixels) — one per header column
    col_widths = [60, 100, 110, 65, 180, 160, 65, 180, 180, 170, 80, 180, 75, 150]
    width_requests = [
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sid,
                    "dimension": "COLUMNS",
                    "startIndex": i,
                    "endIndex": i + 1
                },
                "properties": {"pixelSize": w},
                "fields": "pixelSize"
            }
        }
        for i, w in enumerate(col_widths)
    ]

    # Freeze header row
    freeze_request = {
        "updateSheetProperties": {
            "properties": {
                "sheetId": sid,
                "gridProperties": {"frozenRowCount": 1}
            },
            "fields": "gridProperties.frozenRowCount"
        }
    }

    # Checkbox data validation for checkbox columns
    checkbox_requests = [
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 1,
                    "endRowIndex": 500,
                    "startColumnIndex": col,
                    "endColumnIndex": col + 1
                },
                "rule": {
                    "condition": {"type": "BOOLEAN"},
                    "showCustomUi": True
                }
            }
        }
        for col in CHECKBOX_COLS
    ]

    spreadsheet.batch_update({
        "requests": [freeze_request] + width_requests + checkbox_requests
    })

    print("Sheet set up with Bell branding.")


# ── colour a data row ──────────────────────────────────────────────────────────

def colour_row(spreadsheet: gspread.Spreadsheet, ws: gspread.Worksheet, row_num: int):
    bg = LIGHT_GREY if row_num % 2 == 0 else WHITE
    spreadsheet.batch_update({
        "requests": [{
            "repeatCell": {
                "range": {
                    "sheetId": ws.id,
                    "startRowIndex": row_num - 1,
                    "endRowIndex": row_num,
                    "startColumnIndex": 0,
                    "endColumnIndex": len(HEADERS)
                },
                "cell": {
                    "userEnteredFormat": {"backgroundColor": bg}
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        }]
    })


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        print("ERROR: GOOGLE_SHEET_ID not set in .env")
        raise SystemExit(1)

    if not CREDENTIALS_PATH.exists():
        print("ERROR: credentials.json not found in project root.")
        raise SystemExit(1)

    print("Connecting to Google Sheets...")
    client      = get_client()
    spreadsheet = client.open_by_key(sheet_id)
    ws          = spreadsheet.sheet1

    # First-run setup if headers are missing
    if not ws.row_values(1) or ws.cell(1, 1).value != "Week #":
        print("First run — formatting sheet...")
        setup_sheet(spreadsheet, ws)

    week_num, project_title, skill = get_curriculum_info()
    saas_task = get_saas_task()
    today     = datetime.now().strftime("%Y-%m-%d")
    saturday  = next_saturday()

    row = [
        week_num, today, saturday,
        False,                  # ✓ Sent
        project_title, skill,
        False,                  # ✓ Built
        "", "", "",             # product placeholders
        False,                  # ✓ Products Created
        saas_task,
        False,                  # ✓ SaaS Done
        ""                      # Notes
    ]

    # Find the actual last row with data in column A (ignores validation-only rows)
    col_a = ws.col_values(1)
    new_row_num = len(col_a) + 1
    cell_range = f"A{new_row_num}:{chr(64 + len(HEADERS))}{new_row_num}"
    ws.update(values=[row], range_name=cell_range, value_input_option="USER_ENTERED")

    colour_row(spreadsheet, ws, new_row_num)

    print(f"✓ Week {week_num} logged to Bell Newsletter Tracker (row {new_row_num})")
    print(f"  Project : {project_title}")
    print(f"  Deadline: {saturday}")
    print(f"  SaaS    : {saas_task}")


if __name__ == "__main__":
    main()
