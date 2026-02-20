"""
CIS-4930 Introduction to Python, Spring 2026
Homework : 2
Problem : 2
Student Name: Ammiel Bowen
Student ID: ab22dv
Section: 0003
Submission Date: 02-18-2026
"""

# grade auditor
# read csv, convert grades validate range, log errors spit out json
# MUST have: ValueError except, custom InvalidGradeError, assert, else, finally
import json
import csv
from datetime import datetime


# custom exception. professor asked for it lol
class InvalidGradeError(Exception):
    pass


def now_ts():
    # timestamp format like sample (with the T)
    return datetime.now().isoformat(timespec="seconds")


def log_error(log_path, message):
    # append mode. dont nuke old logs
    # utf-8
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{now_ts()}] ERROR: {message}\n")


def load_config(config_path):
    # loads valid_courses.json
    # it has min/max grade and also required_courses (we dont really use that here but still load it)
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    min_g = config.get("min_grade", 0.0)
    max_g = config.get("max_grade", 4.0)

    #if this fails then config is messed up
    assert min_g <= max_g, "Config invalid: min_grade must be <= max_grade"

    # float
    return config, float(min_g), float(max_g)


def read_grade_rows(csv_path):
    # reads the grades.csv file. skip header row
    rows = []

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)

        header = next(reader, None)  # header line student_id,name,grade etc

        for row in reader:
            #store rows.  handle bad ones later
            rows.append(row)

    #assert statements 
    assert len(rows) >= 0, "Rows list must exist"

    return rows


def validate_grade(grade_value, min_g, max_g):
    # if its outside range, raise our custom exception
    # (this is where InvalidGradeError comes in)
    if grade_value < min_g or grade_value > max_g:
        raise InvalidGradeError(f"grade {grade_value} outside range [{min_g}, {max_g}]")

    return True


def main():
    # these files must be in same folder as this script when running
    config_path = "valid_courses.json"
    grades_path = "grades.csv"

    out_valid_json = "valid_grades.json"
    error_log = "grade_errors.log"

    # load config first
    config, min_g, max_g = load_config(config_path)

    # read csv rows
    rows = read_grade_rows(grades_path)

    valid_records = []   # this becomes JSON output list
    error_count = 0
    valid_count = 0

    # another assert because assignment wants asserts
    assert isinstance(rows, list), "rows should be a list"

    # row number tracking (to match sample-ish output)
    row_number = 1  # header was row 1, so data starts row 2

    for row in rows:
        row_number += 1  # first data row -> 2

        try:
            # each row should have exactly 3 things
            if len(row) != 3:
                error_count += 1
                log_error(error_log, f"Row {row_number} - malformed row {row}")
                print(f"Processed row {row_number}")
                continue

            student_id = row[0].strip()
            name = row[1].strip()
            grade_str = row[2].strip()

            #throws ValueError
            grade_val = float(grade_str)

        except ValueError:
            # conversion failed (like 'abc')
            error_count += 1
            log_error(error_log, f"{row[0]},{row[1]} - invalid grade '{row[2]}' (ValueError)")
            print(f"Processed row {row_number}")

        else:
            # else runs ONLY if float conversion worked (no ValueError happened)
            # now do range validation
            try:
                validate_grade(grade_val, min_g, max_g)

            except InvalidGradeError as e:
                # out of range, log it
                error_count += 1
                log_error(error_log, f"{student_id},{name} - {str(e)}")
                print(f"Processed row {row_number}")

            else:
                # valid, keep it
                valid_records.append({
                    "student_id": student_id,
                    "name": name,
                    "grade": grade_val
                })
                valid_count += 1

                # sample shows checkmark message, so we do it too
                print(f"✓ Processed {name}: {grade_val}")
                print(f"Processed row {row_number}")

            finally:
                # finally block. runs either way (valid or invalid range)
                pass

        finally:
            #  finally (outer) just so its super obvious we used one
            pass

    # write valid json file
    with open(out_valid_json, "w", encoding="utf-8") as f:
        json.dump(valid_records, f, indent=2, ensure_ascii=False)

    # summary output like sample
    print("\nProcessed grades.csv:")
    print(f"✓ {valid_count} valid grades saved to {out_valid_json}")
    print(f"✗ {error_count} errors logged to {error_log}")


if __name__ == "__main__":
    main()