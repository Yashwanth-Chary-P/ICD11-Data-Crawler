# ICD-11 Data Crawler

A Python command-line tool for building CSV datasets from the WHO ICD-11 API.
It starts from an ICD-11 chapter or entity ID, walks the entity tree with
depth-first traversal, fetches residual categories such as `other` and
`unspecified`, extracts commonly used classification fields, and writes the
result to a UTF-8 CSV file.

The default configuration points to the WHO ICD-11 MMS release endpoint. The
sample command in this repository writes to `data/outputs/tm2.csv`, which is a
useful output name when crawling TM2-related ICD-11 content.

## What Is ICD-11?

ICD-11 is the 11th revision of the International Classification of Diseases,
published by the World Health Organization. It is the global standard used to
classify diseases, disorders, injuries, symptoms, external causes, and other
health-related concepts.

Health systems, researchers, hospitals, governments, and software platforms use
ICD-11 codes to make health information consistent across records, reporting,
analytics, public-health monitoring, mortality and morbidity statistics, and
interoperable clinical datasets.

## Why This Project Is Useful

The WHO ICD-11 browser and API expose rich structured data, but researchers and
data teams often need a flat file that can be opened in spreadsheets, loaded
into databases, or used in machine-learning and search pipelines. This crawler
automates that conversion.

Use this project when you need to:

- Export ICD-11 chapter or entity data into CSV.
- Build a reusable dataset with ICD codes, titles, descriptions, inclusions,
  exclusions, and index terms.
- Preserve residual categories like `other` and `unspecified`, which are easy
  to miss when only crawling child entities.
- Re-run the extraction against a specific WHO ICD-11 release endpoint.
- Create a clean source file for downstream analytics, validation, search, or
  mapping workflows.

## Features

- Authenticates with the WHO ICD API using client credentials from `.env`.
- Traverses ICD-11 entities recursively with duplicate protection.
- Fetches normal entities and residual `other` / `unspecified` entities.
- Refreshes the access token when the API returns `401 Unauthorized`.
- Exports a deterministic CSV header.
- Creates the output directory automatically.
- Includes focused tests for extraction behavior.

## Project Structure

```text
icd11-crawler/
  src/
    auth.py        # WHO ICD API token handling
    config.py      # Environment-based settings
    crawler.py     # Depth-first ICD entity traversal
    exporter.py    # CSV writer setup
    extractor.py   # API response to CSV row mapping
    icd_client.py  # ICD-11 HTTP client
    main.py        # Command-line entry point
  tests/
    test_extractor.py
  data/
    outputs/       # Generated CSV files are written here
```

## Requirements

- Python 3.10 or newer
- WHO ICD API client credentials

Install the Python dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Fill in your WHO ICD API credentials:

```env
ICD_CLIENT_ID=your-client-id
ICD_CLIENT_SECRET=your-client-secret
```

Optional endpoint overrides are also supported:

```env
ICD_TOKEN_URL=https://icdaccessmanagement.who.int/connect/token
ICD_BASE_URL=https://id.who.int/icd/release/11/2026-01/mms
```

## Usage

Run the crawler with a starting ICD-11 chapter or entity ID:

```bash
python src/main.py --chapter-id 562274788 --output data/outputs/tm2.csv
```

The `--output` argument is optional. If it is omitted, the crawler writes to
`data/outputs/tm2.csv`:

```bash
python src/main.py --chapter-id 562274788
```

## CSV Output

The generated CSV contains these columns:

| Column | Description |
| --- | --- |
| `Code` | ICD-11 code for the entity. |
| `title` | Preferred ICD-11 title. |
| `Fully Specified Name` | Full clinical/classification name when available. |
| `Description` | ICD-11 definition text when available. |
| `Inclusions` | Semicolon-separated inclusion terms. |
| `Exclusions` | Semicolon-separated exclusion terms. |
| `Index Terms` | Semicolon-separated index terms and synonyms. |

Generated CSV files and local credentials are intentionally ignored by Git.

## Running Tests

```bash
pytest
```

## Notes

- The crawler sleeps briefly between entity visits to avoid aggressive request
  bursts.
- If an entity does not contain an ICD code, it is skipped in the CSV output.
- API access depends on valid WHO ICD credentials and the configured release
  endpoint.
