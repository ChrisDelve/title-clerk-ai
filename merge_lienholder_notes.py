import csv
import re
from pathlib import Path


CURRENT_FILE = Path("data/lienholder_internal_notes.csv")
NEW_FILE = Path("data/lienholder_internal_notes_UPDATED_from_bank_contacts.csv")
OUTPUT_FILE = Path("data/lienholder_internal_notes_MERGED.csv")


FIELDNAMES = [
    "display_name",
    "elt_customer_number",
    "phone",
    "email",
    "payoff_website",
    "lien_release_notes",
    "elt_notes",
    "search_aliases",
    "last_verified_date",
    "internal_notes",
]


def normalize_name(value):
    value = str(value or "").upper()
    value = re.sub(r"[^A-Z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def read_csv(path):
    if not path.exists():
        print(f"Missing file: {path}")
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def clean_row(row):
    cleaned = {}

    for field in FIELDNAMES:
        cleaned[field] = str(row.get(field, "") or "").strip()

    return cleaned


def merge_rows(old_row, new_row):
    """
    Merge duplicate bank rows.
    Old/current file wins when it already has info.
    New file fills in blanks.
    """
    merged = {}

    for field in FIELDNAMES:
        old_value = str(old_row.get(field, "") or "").strip()
        new_value = str(new_row.get(field, "") or "").strip()

        if old_value and new_value and old_value != new_value:
            if field == "internal_notes":
                merged[field] = f"{old_value} | {new_value}"
            elif field == "search_aliases":
                merged[field] = f"{old_value} | {new_value}"
            else:
                merged[field] = old_value
        elif old_value:
            merged[field] = old_value
        else:
            merged[field] = new_value

    return merged


def main():
    current_rows = [clean_row(row) for row in read_csv(CURRENT_FILE)]
    new_rows = [clean_row(row) for row in read_csv(NEW_FILE)]

    merged_by_name = {}

    for row in current_rows:
        key = normalize_name(row.get("display_name", ""))

        if not key:
            continue

        merged_by_name[key] = row

    for row in new_rows:
        key = normalize_name(row.get("display_name", ""))

        if not key:
            continue

        if key in merged_by_name:
            merged_by_name[key] = merge_rows(merged_by_name[key], row)
        else:
            merged_by_name[key] = row

    merged_rows = list(merged_by_name.values())
    merged_rows.sort(key=lambda row: row.get("display_name", "").upper())

    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(merged_rows)

    print("Merge complete.")
    print(f"Current rows: {len(current_rows)}")
    print(f"New rows: {len(new_rows)}")
    print(f"Merged rows: {len(merged_rows)}")
    print(f"Created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()