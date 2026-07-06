import json
from datetime import datetime
from pathlib import Path

folders = [
    Path("./json_files"),
]


def normalize_date(date_str: str) -> str:
    """
    Convert a date to 'YYYY-MM-DD HH:MM:SSZ'.
    Accepted input formats:
    - 'YYYY-MM-DD HH:MM:SSZ'
    - 'YYYY-MM-DD'
    - 'dd/mm/yy'
    """
    if not date_str:
        return date_str

    date_str = date_str.strip()

    accepted_formats = (
        "%Y-%m-%d %H:%M:%SZ",
        "%Y-%m-%d",
        "%d/%m/%y",
    )

    for date_format in accepted_formats:
        try:
            dt = datetime.strptime(date_str, date_format)
            return dt.strftime("%Y-%m-%d %H:%M:%SZ")
        except ValueError:
            pass

    raise ValueError(f"Unrecognized date format: {date_str}")


for folder in folders:
    if not folder.exists():
        print(f"Cartella non trovata: {folder}")
        continue

    for file_path in folder.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                print(f"Skippato {file_path}: il contenuto non è una lista.")
                continue

            changed = False

            for match in data:
                if not isinstance(match, dict):
                    continue

                if "DateUtc" in match and match["DateUtc"]:
                    old_date = match["DateUtc"]
                    new_date = normalize_date(old_date)

                    if new_date != old_date:
                        match["DateUtc"] = new_date
                        changed = True

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            if changed:
                print(f"Convertito e sovrascritto: {file_path}")
            else:
                print(f"Nessuna modifica necessaria: {file_path}")

        except Exception as e:
            print(f"Errore nel file {file_path}: {e}")

print("Operazione completata.")
