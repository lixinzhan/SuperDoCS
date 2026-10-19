import csv
import hashlib
import sys


def csv_valid(fname):
    try:
        with open(fname, 'r', encoding='utf-8-sig', newline='') as csvfile:
            freader = csv.reader(csvfile)
            title = next(freader, None)
            row = next(freader, None)
            checksum_row = next(freader, None)
            extra_row = next(freader, None)
    except (OSError, UnicodeError, csv.Error):
        return False

    # The exporter writes a header, one data row, and a one-cell checksum row.
    if (not title or not row or len(title) != len(row)
            or checksum_row is None or len(checksum_row) != 1
            or extra_row is not None):
        return False

    # Match the exporter's checksum input: the comma-joined data fields in UTF-8.
    md5input = ','.join(row)
    md5output = hashlib.md5(md5input.encode('utf-8')).hexdigest()
    return md5output == checksum_row[0]


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        print('Usage: verifychecksum.py CSV_FILE', file=sys.stderr)
        return 2

    if csv_valid(argv[0]):
        print('CSV checksum passed!')
        return 0

    print('CSV checksum failed!')
    return 1


if __name__ == '__main__':
    sys.exit(main())
