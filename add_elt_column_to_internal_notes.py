import csv
from pathlib import Path


ACTIVE_FILE = Path("data/lienholder_internal_notes.csv")
BACKUP_FILE = Path("data/lienholder_internal_notes_BEFORE_ELT_COLUMN.csv")


def main():
    if not ACTIVE_FILE.exists():
        print(f"Missing file: {ACTIVE_FILE}")
        return

    # Backup current active file
    BACKUP_FILE.write_bytes(ACTIVE_FILE.read_bytes())

    with ACTIVE_FILE.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    if "elt_customer_number" not in fieldnames:
        # Put elt_customer_number right after display_name
        new_fieldnames = []

        for field in fieldnames:
            new_fieldnames.append(field)

            if field == "display_name":
                new_fieldnames.append("elt_customer_number")

        fieldnames = new_fieldnames

        for row in rows:
            row["elt_customer_number"] = ""

    # Set preferred Honda ELT customer number
    for row in rows:
        display_name = str(row.get("display_name", "") or "").strip().upper()

        if display_name == "AMERICAN HONDA FINANCE CORPORATION":
            row["elt_customer_number"] = "200010258"

    with ACTIVE_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Done.")
    print(f"Backup created: {BACKUP_FILE}")
    print(f"Updated active file: {ACTIVE_FILE}")
    print("Honda preferred ELT customer number set to 200010258.")


if __name__ == "__main__":
    main()