"""
Lambda: Submit Arca AI contact form → append to S3 CSV.
Triggered via Function URL (HTTP POST).
"""
import csv
import io
import json
import os
from datetime import datetime, timezone

import boto3

S3_BUCKET = os.environ["CONTACTS_BUCKET"]
S3_KEY = "contacts.csv"

s3 = boto3.client("s3")


def _csv_rows_to_string(rows: list[list[str]]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerows(rows)
    return buf.getvalue()


def _load_existing_csv() -> list[list[str]]:
    """Download contacts.csv from S3. Return rows (list of lists)."""
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        content = obj["Body"].read().decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        return list(reader)
    except s3.exceptions.NoSuchKey:
        return []  # No file yet


def _save_csv(rows: list[list[str]]) -> None:
    body = _csv_rows_to_string(rows)
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY,
        Body=body.encode("utf-8"),
        ContentType="text/csv",
    )


def handler(event: dict, context) -> dict:
    headers = {"Content-Type": "application/json"}

    # ── CORS preflight ──────────────────────────────────────────
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}

    # ── Parse body ──────────────────────────────────────────────
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {"statusCode": 400, "headers": headers, "body": json.dumps({"error": "Invalid JSON"})}

    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip()
    company = (body.get("company") or "").strip()
    message = (body.get("message") or "").strip()

    if not name or not email:
        return {"statusCode": 422, "headers": headers, "body": json.dumps({"error": "name and email are required"})}

    # ── Append row ──────────────────────────────────────────────
    rows = _load_existing_csv()

    # Add header if new file
    if not rows:
        rows.append(["timestamp", "name", "email", "company", "message"])

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows.append([ts, name, email, company, message])

    _save_csv(rows)

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps({"ok": True, "count": len(rows) - 1}),
    }
