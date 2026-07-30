import json
import locale
import sys
import unicodedata
from pathlib import Path

locale.setlocale(locale.LC_COLLATE, 'en_US.UTF-8')


def normalise_string(string: str) -> str:
    # Normalise any unicode characters in the string to
    # allow alphabetical sorting to work.
    return ''.join(c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn')


# Loop through all of the files in the data directory.
# Note that this script will be run from the root directory.
files = Path("data/").glob("*.json")

for file in files:
    print(f"Validating {file.name}")
    with Path(file).open(encoding='utf-8') as f:
        data: list[str] = json.load(f)

        # Make sure the file doesn't include any duplicate values.
        if len(data) != len(set(data)):
            sys.exit(f"{file} contains duplicate entries")

        # Make sure the values are in alphabetical order.
        sorted_data: list[str] = sorted(data, key=normalise_string)

        if data != sorted_data:
            for i, d in enumerate(data):
                if d != sorted_data[i]:
                    print(d)
                    print(sorted_data[i])
            sys.exit(f"{file} is not in alphabetical order")
