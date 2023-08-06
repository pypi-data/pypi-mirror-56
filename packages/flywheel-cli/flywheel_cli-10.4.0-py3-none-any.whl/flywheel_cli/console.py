"""Provide helpers for printing to the console"""


def print_table(out, table):
    """Table printer"""
    # Calculate max width
    widths = [0] * len(table[0])
    for row in table:
        for i, col in enumerate(row):
            widths[i] = max(widths[i], len(col))

    for row in table:
        for i, col in enumerate(row):
            print(col.ljust(widths[i]), end=' ', file=out)
        print(file=out)
