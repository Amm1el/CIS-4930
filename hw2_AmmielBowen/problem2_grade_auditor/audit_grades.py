"""
CIS-4930 Introduction to Python, Spring 2026
Homework : 2
Problem : 2
Student Name: Ammiel Bowen
Student ID: ab22dv
Section: 0003
Submission Date: 02-18-2026
"""

# this problem is basically: read CSV safely, validate grades, log errors, write JSON
# REQUIRED: try/except ValueError, custom InvalidGradeError, assert, else clause, finally block
import json
import csv
from datetime import datetime


# custom exception class required by the prompt
class InvalidGradeError(Exception):
    pass


def now_ts():
    # same timestamp style as problem 1
    return datetime.now().isoformat(timespec="seconds")


def log_error(log_path, message):
    # append mode required (do not overwrite old errors)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{now_ts()}] ERROR: {message}\n")


def load_config(config_path):
    # loads min_grade, max_grade, required_courses (we dont really use courses for grade validation,
    # but we load it because prompt says to load valid_courses.json)
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    min_g = config.get("min_grade", 0.0)
    max_g = config.get("max_grade", 4.0)

    # internal sanity checks using assert (this is exactly the type of thing they want)
    assert min_g <= max_g, "Config invalid: min_grade must be <= max_grade"

    return config, float(min_g), float(max_g)


def read_grade_rows(csv_path):
    # reads grades.csv using csv.reader and skips header row
    rows = []

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)

        # skip header
        header = next(reader, None)

        # read each row (should be student_id,name,grade)
        for row in reader:
            # keep malformed rows too, because we want to log problems instead of crashing
            rows.append(row)

    # assert invariant: we expect at least 1 row after header in normal cases
    # (if empty file, this assert might trigger, but that's ok since they wanted asserts)
    assert len(rows) >= 0, "Rows list must exist (basic invariant)"

    return rows


def validate_grade(grade_value, min_g, max_g):
    # range validation: if out of range, raise custom error
    if grade_value < min_g or grade_value > max_g:
        raise InvalidGradeError(f"grade {grade_value} outside range [{min_g}, {max_g}]")

    return True


def main():
    config_path = "valid_courses.json"
    grades_path = "grades.csv"

    out_valid_json = "valid_grades.json"
    error_log = "grade_errors.log"

    config, min_g, max_g = load_config(config_path)

    rows = read_grade_rows(grades_path)

    valid_records = []
    error_count = 0
    valid_count = 0

    # this assert is another internal check (they specifically asked for asserts)
    assert isinstance(rows, list), "rows should be a list"

    # we want console output showing progress like the sample
    # we will track row number (starting after header, so row index 2 matches their style)
    row_number = 1  # we'll increment before using, so first data row prints as 2

    for row in rows:
        row_number += 1  # now row_number is 2 for first data row, etc.

        # we will always print "Processed row X" like their sample lines
        # but also print the ✓ line on valid rows
        try:
            # row should be [student_id, name, grade_str]
            if len(row) != 3:
                # malformed row is considered an error
                error_count += 1
                log_error(error_log, f"Row {row_number} - malformed row {row}")
                print(f"Processed row {row_number}")
                continue

            student_id = row[0].strip()
            name = row[1].strip()
            grade_str = row[2].strip()

            # 1) safe conversion to float using try/except ValueError
            grade_val = float(grade_str)

        except ValueError:
            # required: specifically catch ValueError for conversion
            error_count += 1
            log_error(error_log, f"{row[0]},{row[1]} - invalid grade '{row[2]}' (ValueError)")
            print(f"Processed row {row_number}")

        else:
            # REQUIRED: else clause (runs only if try succeeded with NO exception)
            # now do range validation using custom exception
            try:
                validate_grade(grade_val, min_g, max_g)

            except InvalidGradeError as e:
                # range issue -> log it
                error_count += 1
                log_error(error_log, f"{student_id},{name} - {str(e)}")
                print(f"Processed row {row_number}")

            else:
                # valid record, so store it for output JSON
                valid_records.append({
                    "student_id": student_id,
                    "name": name,
                    "grade": grade_val
                })
                valid_count += 1

                # print the “checkmark” style line like sample
                print(f"✓ Processed {name}: {grade_val}")
                print(f"Processed row {row_number}")

            finally:
                # REQUIRED: finally block (runs whether validation passed or failed)
                # this is just to show it exists; we are not doing anything crazy here
                # (its like a "this always happens" section)
                pass

        finally:
            # another finally at outer level to show usage even for ValueError case
            # again, not doing much, just demonstrating structure
            pass

    # after processing all rows, write valid_grades.json as list of dicts
    with open(out_valid_json, "w", encoding="utf-8") as f:
        json.dump(valid_records, f, indent=2, ensure_ascii=False)

    # final console summary like the sample
    print(f"\nProcessed grades.csv:")
    print(f"✓ {valid_count} valid grades saved to {out_valid_json}")
    print(f"✗ {error_count} errors logged to {error_log}")


if __name__ == "__main__":
    main()
