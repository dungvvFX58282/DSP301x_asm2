"""Test Grade Calculator - DSP301x Assignment 2.

Read a class answer file (e.g. class1.txt), check every line, grade the
valid answer sheets, print a statistics report and save each student's
score to <class>_grades.txt.

Author: Vu Viet Dung (dungvvFX58282)
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

# Data files live next to this script, whatever the current folder is.
DATA_DIR = Path(__file__).resolve().parent

ANSWER_KEY = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
NUM_VALUES = 26             # 1 student ID + 25 answers
ID_PATTERN = r"N\d{8}"      # "N" followed by exactly 8 digits
HIGH_SCORE = 80             # a score strictly above this counts as high
POINTS_CORRECT = 4
POINTS_WRONG = -1           # a skipped answer gives 0 points


def open_class_file():
    """Task 1: ask for a class name until its file can be opened.

    Return (class name, Series with one raw line of the file per row).
    """
    while True:
        name = input("Enter a class to grade (i.e. class1 for class1.txt): ")
        name = name.strip()
        if name.lower().endswith(".txt"):
            name = name[:-4]
        try:
            # Each line is read as one whole string: the tab separator and
            # QUOTE_NONE keep pandas from splitting or interpreting it, so
            # broken lines with too many or too few values still load.
            lines = pd.read_csv(DATA_DIR / f"{name}.txt", header=None,
                                names=["raw"], sep="\t", dtype=str,
                                quoting=csv.QUOTE_NONE,
                                keep_default_na=False)["raw"]
        except (FileNotFoundError, IsADirectoryError, PermissionError):
            print("File cannot be found.")
        except pd.errors.EmptyDataError:
            print(f"{name}.txt is empty.")
        else:
            print(f"Successfully opened {name}.txt")
            return name, lines.str.strip()


def analyze_lines(lines):
    """Task 2: validate every line and report the invalid ones.

    Return a DataFrame of the valid lines: column "id" plus columns
    1..25 holding each answer ("" when the question was skipped).
    """
    print("\n**** ANALYZING ****\n")
    values = lines.str.split(",")
    count_ok = values.str.len() == NUM_VALUES
    id_ok = values.str[0].str.fullmatch(ID_PATTERN)
    valid = count_ok & id_ok

    # Report invalid lines in file order; a wrong number of values is
    # checked first because the ID is meaningless on a broken line.
    for idx in lines.index[~valid]:
        if not count_ok[idx]:
            print(f"Invalid line of data: does not contain exactly "
                  f"{NUM_VALUES} values:")
        else:
            print("Invalid line of data: N# is invalid")
        print(lines[idx] + "\n")
    if valid.all():
        print("No errors found!\n")

    print("\n**** REPORT ****\n")
    print(f"Total valid lines of data: {int(valid.sum())}")
    print(f"Total invalid lines of data: {int((~valid).sum())}\n")

    sheets = pd.DataFrame(values[valid].tolist(),
                          columns=["id"] + list(range(1, NUM_VALUES)))
    return sheets


def grade(sheets):
    """Task 3: score each sheet with numpy.

    Return (scores as a Series indexed like sheets,
            boolean matrix of skipped answers,
            boolean matrix of wrong answers).
    """
    answers = sheets.drop(columns="id").to_numpy()     # shape (n, 25)
    key = np.array(ANSWER_KEY.split(","))               # shape (25,)
    skipped = answers == ""
    correct = answers == key                            # broadcast per row
    wrong = ~correct & ~skipped
    scores = (POINTS_CORRECT * correct.sum(axis=1)
              + POINTS_WRONG * wrong.sum(axis=1))
    return pd.Series(scores, index=sheets.index), skipped, wrong


def most_common(flags):
    """List the question(s) with the highest count in a boolean matrix.

    Ties are all listed, as "question - count - ratio" (ratio of the
    valid sheets, rounded to 3 decimals).
    """
    counts = flags.sum(axis=0)          # one count per question
    top = counts.max()
    if top == 0:
        return "none"
    questions = np.flatnonzero(counts == top) + 1       # 1-based numbers
    ratio = round(top / len(flags), 3)
    return ", ".join(f"{q} - {top} - {ratio}" for q in questions)


def report_statistics(scores, skipped, wrong):
    """Task 3.1 - 3.8: print the class statistics."""
    if scores.empty:
        print("No valid answer sheet to grade.")
        return
    median = scores.median()
    # The median of an even number of scores can be x.5; keep it then.
    median = int(median) if float(median).is_integer() else round(median, 3)
    print(f"Total student of high scores: {int((scores > HIGH_SCORE).sum())}")
    print(f"Mean (average) score: {scores.mean():.2f}")
    print(f"Highest score: {scores.max()}")
    print(f"Lowest score: {scores.min()}")
    print(f"Range of scores: {scores.max() - scores.min()}")
    print(f"Median score: {median}")
    print(f"Question that most people skip: {most_common(skipped)}")
    print("Question that most people answer incorrectly: "
          f"{most_common(wrong)}")


def save_grades(name, sheets, scores):
    """Task 4: write "ID,score" lines to <class>_grades.txt."""
    out_path = DATA_DIR / f"{name}_grades.txt"
    result = pd.DataFrame({"id": sheets["id"], "score": scores})
    result.to_csv(out_path, header=False, index=False, lineterminator="\n")
    print(f"\nSaved grades to {out_path.name}")


def main():
    name, lines = open_class_file()
    sheets = analyze_lines(lines)
    scores, skipped, wrong = grade(sheets)
    report_statistics(scores, skipped, wrong)
    save_grades(name, sheets, scores)


if __name__ == "__main__":
    main()
