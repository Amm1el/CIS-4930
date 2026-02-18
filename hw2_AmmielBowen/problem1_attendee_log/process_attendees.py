"""
CIS-4930 Introduction to Python, Spring 2026
Homework : 2
Problem : 1
Student Name: Ammiel Bowen
Student ID: ab22dv
Section: 0003
Submission Date: 02-18-2026
"""

# this problem is mainly about file I/O + merging data without duplicates + logging
# we are REQUIRED to use json module and csv module, and open everything with UTF-8
import json
import csv
from datetime import datetime


# helper function to make timestamps like: 2026-02-08T21:57:50
def now_ts():
    # datetime.now().isoformat() gives the "T" format they show in the sample
    # timespec="seconds" keeps it clean (no microseconds)
    return datetime.now().isoformat(timespec="seconds")


def log_event(log_file, message):
    # log file MUST be append mode so we do not overwrite old log entries
    # also required: encoding="utf-8"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{now_ts()}] PROCESS: {message}\n")


def load_config(config_path):
    # config.json contains:
    # {
    #   "log_file": "conference.log",
    #   "vip_ids": ["A001", "A004", "A010"]
    # }
    # requirement: uses json.load and UTF-8
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # if the json is missing something, we still want to not crash
    # .get lets us provide defaults
    log_file = config.get("log_file", "conference.log")
    vip_ids = config.get("vip_ids", [])

    return log_file, vip_ids


def read_attendees_raw(txt_path):
    # attendees_raw.txt format: id,name,email per line
    # requirement: read line-by-line and parse comma-separated values
    attendees_by_id = {}  # dict keyed by id makes it easy to avoid duplicates later

    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            # strip removes newline and extra spaces
            line = line.strip()

            # skip blank lines just in case file has empty rows
            if line == "":
                continue

            # split by commas; expected 3 parts
            parts = line.split(",")

            # basic edge case: if line is malformed, ignore it (bonus-safe)
            if len(parts) != 3:
                continue

            attendee_id = parts[0].strip()
            name = parts[1].strip()
            email = parts[2].strip()

            # only add if id is non-empty
            if attendee_id != "":
                attendees_by_id[attendee_id] = {
                    "id": attendee_id,
                    "name": name,
                    "email": email
                }

    return attendees_by_id


def merge_new_registrations(attendees_by_id, csv_path):
    # new_registrations.csv has a header row: id,name,email
    # requirement: use csv.reader and skip header
    merged_count = 0

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)

        # skip header row
        header = next(reader, None)

        # go through each CSV row after the header
        for row in reader:
            # expected 3 columns: id, name, email
            if len(row) != 3:
                # ignore malformed rows (bonus-safe)
                continue

            attendee_id = row[0].strip()
            name = row[1].strip()
            email = row[2].strip()

            # dedup rule: do NOT create duplicates by id, preserve originals
            if attendee_id == "":
                continue

            if attendee_id not in attendees_by_id:
                attendees_by_id[attendee_id] = {
                    "id": attendee_id,
                    "name": name,
                    "email": email
                }
                merged_count += 1
            else:
                # if already exists, we do nothing (preserve original record)
                pass

    return merged_count


def write_attendees_final(attendees_by_id, output_json_path):
    # requirement: JSON list of dicts sorted by id, indent=2
    # also requirement: do NOT modify source incorrectly; we are building a new list
    sorted_ids = sorted(attendees_by_id.keys())

    final_list = []
    for attendee_id in sorted_ids:
        final_list.append(attendees_by_id[attendee_id])

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)  # ensure_ascii=False keeps accents

    return len(final_list)


def write_vip_report(attendees_by_id, vip_ids, vip_report_path):
    # vip report format example:
    # A001: Alice García <alice@example.com>
    # A010: NOT FOUND
    with open(vip_report_path, "w", encoding="utf-8") as f:
        for vip_id in vip_ids:
            if vip_id in attendees_by_id:
                person = attendees_by_id[vip_id]
                f.write(f"{vip_id}: {person['name']} <{person['email']}>\n")
            else:
                f.write(f"{vip_id}: NOT FOUND\n")

    return len(vip_ids)


def main():
    # file names are expected to be in the SAME folder as this script
    config_path = "config.json"
    raw_path = "attendees_raw.txt"
    new_csv_path = "new_registrations.csv"

    out_final_json = "attendees_final.json"
    out_vip_report = "vip_report.txt"

    # 1) load config first, because it tells us what log file to use
    log_file, vip_ids = load_config(config_path)
    log_event(log_file, "Loaded configuration")

    # 2) load raw attendees
    attendees_by_id = read_attendees_raw(raw_path)
    log_event(log_file, f"Loaded {len(attendees_by_id)} attendees from attendees_raw.txt")

    # 3) merge new registrations without duplicates
    merged_count = merge_new_registrations(attendees_by_id, new_csv_path)
    log_event(log_file, f"Merged {merged_count} new attendees from new_registrations.csv")

    # 4) write final JSON sorted by id
    total_count = write_attendees_final(attendees_by_id, out_final_json)
    log_event(log_file, f"Wrote {total_count} total attendees to attendees_final.json")

    # 5) write VIP report even if some are missing (NOT FOUND)
    vip_count = write_vip_report(attendees_by_id, vip_ids, out_vip_report)
    log_event(log_file, f"Wrote VIP report for {vip_count} IDs to vip_report.txt")

    # small console message just so we see it ran
    print("Done. Outputs generated:")
    print("-", log_file)
    print("-", out_final_json)
    print("-", out_vip_report)


# standard python main guard (keeps it clean if imported, but we run directly)
if __name__ == "__main__":
    main()
