"""
CIS-4930 Introduction to Python, Spring 2026
Homework : 2
Problem : 1
Student Name: Ammiel Bowen
Student ID: ab22dv
Section: 0003
Submission Date: 02-18-2026
"""

# need json + csv
import json
import csv
from datetime import datetime


# quick helper for timestamp (so log looks like sample)
def now_ts():
    # iso format gives that T between date and time
    # timespec keeps it from getting crazy long with decimals
    return datetime.now().isoformat(timespec="seconds")


def log_event(log_file, message):
    # must append mode. do NOT overwrite old logs
    # utf-8 because accents
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{now_ts()}] PROCESS: {message}\n")


def load_config(config_path):
    # config.json holds log file name + vip list
    # using json.load because that’s required
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # .get for if key missing
    log_file = config.get("log_file", "conference.log")
    vip_ids = config.get("vip_ids", [])

    return log_file, vip_ids


def read_attendees_raw(txt_path):
    # raw file: id,name,email
    # one per line
    attendees_by_id = {}  # easier to deduce this way

    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()  # remove newline

            if line == "":
                continue

            parts = line.split(",")

            if len(parts) != 3:
                continue

            attendee_id = parts[0].strip()
            name = parts[1].strip()
            email = parts[2].strip()

            if attendee_id != "":
                # storing as dict
                attendees_by_id[attendee_id] = {
                    "id": attendee_id,
                    "name": name,
                    "email": email
                }

    return attendees_by_id


def merge_new_registrations(attendees_by_id, csv_path):
    # CSV has header row
    # must use csv.reader
    merged_count = 0

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)

        header = next(reader, None)  # skip header

        for row in reader:
            # expect 3 columns
            if len(row) != 3:
                continue

            attendee_id = row[0].strip()
            name = row[1].strip()
            email = row[2].strip()

            if attendee_id == "":
                continue

            # important: no duplicates by id
            if attendee_id not in attendees_by_id:
                attendees_by_id[attendee_id] = {
                    "id": attendee_id,
                    "name": name,
                    "email": email
                }
                merged_count += 1
            else:
                # already exists. leave original alone
                pass

    return merged_count


def write_attendees_final(attendees_by_id, output_json_path):
    # sort id alphabetically
    sorted_ids = sorted(attendees_by_id.keys())

    final_list = []

    for attendee_id in sorted_ids:
        final_list.append(attendees_by_id[attendee_id])

    # ensure_ascii False so accented characters stay normal
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)

    return len(final_list)


def write_vip_report(attendees_by_id, vip_ids, vip_report_path):
    #write VIP file
    # if id not found, say NOT FOUND (sample does that)
    with open(vip_report_path, "w", encoding="utf-8") as f:
        for vip_id in vip_ids:
            if vip_id in attendees_by_id:
                person = attendees_by_id[vip_id]
                f.write(f"{vip_id}: {person['name']} <{person['email']}>\n")
            else:
                f.write(f"{vip_id}: NOT FOUND\n")

    return len(vip_ids)


def main():
    #files same folder as script
    config_path = "config.json"
    raw_path = "attendees_raw.txt"
    new_csv_path = "new_registrations.csv"

    out_final_json = "attendees_final.json"
    out_vip_report = "vip_report.txt"

    # load config
    log_file, vip_ids = load_config(config_path)
    log_event(log_file, "Loaded configuration")

    # load existing attendees
    attendees_by_id = read_attendees_raw(raw_path)
    log_event(log_file, f"Loaded {len(attendees_by_id)} attendees from attendees_raw.txt")

    # merge new
    merged_count = merge_new_registrations(attendees_by_id, new_csv_path)
    log_event(log_file, f"Merged {merged_count} new attendees from new_registrations.csv")

    #  final json
    total_count = write_attendees_final(attendees_by_id, out_final_json)
    log_event(log_file, f"Wrote {total_count} total attendees to attendees_final.json")

    # vip 
    vip_count = write_vip_report(attendees_by_id, vip_ids, out_vip_report)
    log_event(log_file, f"Wrote VIP report for {vip_count} IDs to vip_report.txt")

    print("Done.")
    print("Generated:", log_file, out_final_json, out_vip_report)


if __name__ == "__main__":
    main()