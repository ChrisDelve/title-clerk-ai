import csv
import re
from pathlib import Path


ACTIVE_FILE = Path("data/lienholder_internal_notes.csv")
BACKUP_FILE = Path("data/lienholder_internal_notes_BEFORE_EMAIL_CLEANUP.csv")
OUTPUT_FILE = Path("data/lienholder_internal_notes_CLEANED.csv")


GENERIC_EMAIL_KEYWORDS = [
    "dealer",
    "assist",
    "title",
    "titles",
    "lien",
    "liens",
    "release",
    "releases",
    "payoff",
    "payoffs",
    "customer",
    "service",
    "services",
    "support",
    "info",
    "auto",
    "finance",
    "documents",
    "docs",
    "claims",
    "department",
    "dept",
]


EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def is_generic_email(email):
    local_part = email.split("@")[0].lower()

    # Remove separators to catch things like dealer.assist, dealer_assist, title-dept
    compact_local = re.sub(r"[^a-z0-9]", "", local_part)

    for keyword in GENERIC_EMAIL_KEYWORDS:
        if keyword in local_part or keyword in compact_local:
            return True

    return False


def clean_email_field(value):
    emails = EMAIL_PATTERN.findall(value or "")

    generic_emails = []
    for email in emails:
        cleaned_email = email.strip()
        if is_generic_email(cleaned_email):
            generic_emails.append(cleaned_email)

    # Deduplicate while preserving order
    seen = set()
    final_emails = []
    for email in generic_emails:
        key = email.lower()
        if key not in seen:
            seen.add(key)
            final_emails.append(email)

    return " ".join(final_emails)


def clean_internal_notes(value):
    text = str(value or "").strip()

    # Remove any email addresses from internal notes
    text = EMAIL_PATTERN.sub("", text)

    # Remove specific contact names section if present
    text = re.sub(
        r"\|\s*Specific Contact\(s\):.*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"Specific Contact\(s\):.*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Clean extra separators/spaces
    text = re.sub(r"\s+\|\s+\|", " | ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    text = text.strip("|").strip()

    return text


def main():
    if not ACTIVE_FILE.exists():
        print(f"Missing active file: {ACTIVE_FILE}")
        return

    # Backup current active file
    BACKUP_FILE.write_bytes(ACTIVE_FILE.read_bytes())

    with ACTIVE_FILE.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    cleaned_rows = []

    for row in rows:
        row["email"] = clean_email_field(row.get("email", ""))
        row["internal_notes"] = clean_internal_notes(row.get("internal_notes", ""))
        cleaned_rows.append(row)

    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print("Email cleanup complete.")
    print(f"Rows cleaned: {len(cleaned_rows)}")
    print(f"Backup created: {BACKUP_FILE}")
    print(f"Cleaned file created: {OUTPUT_FILE}")
    print("")
    print("Next step:")
    print(f"Rename {OUTPUT_FILE} to {ACTIVE_FILE}")


if __name__ == "__main__":
    main()