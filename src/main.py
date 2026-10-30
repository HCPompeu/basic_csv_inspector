#BASIC .CSV INSPECTOR

import csv
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
input_dir = base_dir / 'data' / 'input'

def list_csv_files():
    try:
        if not input_dir.is_dir():
            print(f'ERROR: input directory not found: {input_dir}')
            return None
        csv_files = [path for path in input_dir.iterdir() if path.is_file() and path.suffix.lower() == '.csv']
        return sorted(csv_files, key=lambda path: path.name.lower())
    except OSError as error:
        print(f'ERROR accessing the input directory: {error}')
        return None

def select_csv_file():
    csv_files = list_csv_files()
    if csv_files is None:
        return None
    if not csv_files:
        print(f'No CSV files found in {input_dir}')
        return None
    print('\nAVAILABLE CSV FILES')
    for index, file_path in enumerate(csv_files, start=1):
        print(f'{index}. {file_path.name}')
    print('0. Exit')
    while True:
        choice = input('Select a file by number: ').strip()
        if choice == '0':
            return None
        if not choice.isdigit():
            print('ERROR: enter a valid number')
            continue
        selection = int(choice)
        if 1 <= selection <= len(csv_files):
            return csv_files[selection - 1]
        print('ERROR: selection out of range')

def inspect_csv(file_path):
    try:
        # Handle UTF-8 BOM and preserve newline handling required by the csv module.
        with file_path.open(mode='r',encoding='utf-8-sig',newline='') as csv_file:
            reader = csv.reader(csv_file, strict=True)
            try:
                columns = next(reader)
            except StopIteration:
                print('ERROR: empty CSV file or missing header')
                return False
            if not columns:
                print('ERROR: empty CSV file or missing header')
                return False
            # Check for unnamed columns
            empty_columns = [index for index, column in enumerate(columns, start=1) if not column.strip()]
            if empty_columns:
                positions = ', '.join(str(index) for index in empty_columns)
                print(f'ERROR: header contains unnamed column(s) at position(s): {positions}')
                return False
            # Check for potentially duplicated column names
            seen_header_names = {}
            duplicate_header_names = []
            for column in columns:
                # Use case-insensitive comparison to flag potentially duplicated column names.
                normalized_name = column.casefold()
                if normalized_name in seen_header_names:
                    original_name = seen_header_names[normalized_name]
                    duplicate_header_names.append((original_name, column))
                else:
                    seen_header_names[normalized_name] = column
            row_count = 0
            missing_counts = [0] * len(columns)
            missing_locations = []
            column_values = [{} for _ in columns]
            extra_locations = []
            total_extra = 0
            previous_line_number = reader.line_num
            for row in reader:
                row_count += 1
                # Track record start lines, including records containing embedded newlines.
                line_number = previous_line_number + 1
                previous_line_number = reader.line_num
                for index, column in enumerate(columns):
                    if index >= len(row):
                        value = ''
                    else:
                        value = row[index]
                    if value.strip() == '':
                        missing_counts[index] += 1
                        missing_locations.append((line_number, column, index + 1))
                    else:
                        # Ignore surrounding whitespace when comparing values within each column.
                        normalized_value = value.strip()
                        if normalized_value not in column_values[index]:
                            column_values[index][normalized_value] = []
                        column_values[index][normalized_value].append(line_number)
                if len(row) > len(columns):
                    extra_values = row[len(columns):]
                    total_extra += len(extra_values)
                    for value in extra_values:
                        extra_locations.append((line_number, value))
    except FileNotFoundError:
        print(f'ERROR: file not found: {file_path}')
        return False
    except PermissionError:
        print(f'ERROR: permission denied: {file_path}')
        return False
    except UnicodeDecodeError:
        print('ERROR: unable to decode the file as UTF-8')
        return False
    except csv.Error as error:
        print(f'ERROR: invalid CSV structure: {error}')
        return False
    except OSError as error:
        print(f'ERROR reading file: {error}')
        return False
    total_missing = sum(missing_counts)
    repeated_values = []
    for index, values in enumerate(column_values):
        for value, lines in values.items():
            if len(lines) > 1:
                repeated_values.append((columns[index], value, lines))
    print('\n===CSV INSPECTION REPORT===')
    print(f'File: {file_path.name}')
    print(f'Number of columns: {len(columns)}')
    print(f'Number of records: {row_count}')
    print(f'Columns: {" | ".join(columns)}')
    print('\n==Data quality warnings==')
    if total_missing == 0 and total_extra == 0:
        print('No data issues detected.')
    else:
        if total_missing > 0:
            print(f'{total_missing} missing value(s).')
        if total_extra > 0:
           print(f'{total_extra} extra value(s).')
    if total_missing > 0:
        print('\n=Missing values=')
        column_counts = ' '.join(f'[{column}: {count}]' for column, count in zip(columns, missing_counts))
        print(column_counts)
        print('Missing values location:')
        for line_number, column, _ in missing_locations:
            print(f'[column: {column} | line: {line_number}]')
    if total_extra > 0:
        print('\n=Extra values=')
        print('Extra values location:')
        for line_number, value in extra_locations:
            print(f'[column: beyond header | line: {line_number} | value: {value}]')
    if duplicate_header_names or repeated_values:
        print('\n=Potential data issues=')
        if duplicate_header_names:
            print('Duplicated column names:')
            for first_name, second_name in duplicate_header_names:
                print(f'[{first_name} / {second_name}]')
        if repeated_values:
            print('Repeated values:')
            for column, value, lines in repeated_values:
                line_numbers = ', '.join(str(line) for line in lines)
                print(f'[column: {column} | value: {value} | lines: {line_numbers}]')
    return True

def main():
    while True:
        file_path = select_csv_file()
        if file_path is None:
            print('Program terminated.')
            break
        inspect_csv(file_path)
        input('\nPress Enter to continue...')
if __name__ == '__main__':
    main()