# Basic CSV Inspector
A Python command-line tool for preliminary inspection of CSV files, identifying structural inconsistencies and potential data quality issues.

The program reads CSV files, performs basic structural checks, and generates an inspection report in the terminal. It does not modify the original files.

## Inspection overview
The program implements the following checks:

- **File discovery and selection:** Lists CSV files in the input directory and allows the user to select a file for inspection.
- **Header validation:** Identifies empty column names and potentially duplicated column names, using case-insensitive comparison.
- **Missing values:** Counts and reports empty values by column and physical line number.
- **Extra values:** Identifies and reports values exceeding the number of columns defined in the header.
- **Repeated values:** Detects repeated non-empty values within individual columns, ignoring leading and trailing whitespace.
- **Error handling:** Handles common file access, encoding, and CSV parsing errors.

The inspection results are displayed directly in the terminal.

## How to use
### Requirements
- Python 3.6 or later.
- No external dependencies. The program uses Python's standard library.

### Run the program
1. Clone or download this repository.
2. Place the CSV files to be inspected in `data/input/`.
3. Navigate to the project directory.
4. Run the main script:

```bash
python src/main.py
```

5. Select a CSV file from the displayed list.

The program reads the selected file and displays the inspection report in the terminal.

## Repository layout
```text
basic-csv-inspector/
├── data/
│   └── input/
├── src/
│   └── main.py
├── .gitignore
├── LICENSE
└── README.md
```

- `data/input/` contains the CSV files to be inspected.
- `src/` contains the Python script implementing the inspection workflow.

## Scope and limitations
Basic CSV Inspector is intended for preliminary structural inspection. It does not perform comprehensive data validation, statistical analysis, or automatic data correction.

Current limitations:

- Uses a comma as the field delimiter.
- Reads files using UTF-8 with BOM support (`utf-8-sig`).
- Repeated values are flagged for inspection but are not necessarily errors.
- Leading and trailing whitespace is ignored when comparing values.
- Potentially duplicated column names are identified through case-insensitive comparison; semantic equivalence between columns is not assessed.
- Does not compare values across columns or identify fully duplicated records.
- Does not modify input files or export inspection reports.
- Stores non-empty values and their line locations during inspection, which may increase memory usage for large files.

## License

See [LICENSE](LICENSE) for the terms governing the use, modification, and redistribution of this project.