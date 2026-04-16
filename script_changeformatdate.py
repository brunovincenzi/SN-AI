import json
from datetime import datetime
from pathlib import Path

folders = [
    Path("./json_files"),
]


def normalize_date(date_str: str) -> str:
    """
    Converte una data da 'dd/mm/yy' a 'YYYY-MM-DD HH:MM:SSZ'.
    Se è già nel formato corretto, la lascia invariata.
    """
    if not date_str:
        return date_str

    date_str = date_str.strip()

    # Già convertita
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%SZ")
        return dt.strftime("%Y-%m-%d %H:%M:%SZ")
    except ValueError:
        pass

    # Formato originale corretto: giorno/mese/anno
    try:
        dt = datetime.strptime(date_str, "%d/%m/%y")
        return dt.strftime("%Y-%m-%d %H:%M:%SZ")
    except ValueError:
        pass

    # Se arriva qui, il formato non è riconosciuto
    raise ValueError(f"Formato data non riconosciuto: {date_str}")


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