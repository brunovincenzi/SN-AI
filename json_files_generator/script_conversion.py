import json
from pathlib import Path

INPUT_DIR = Path('.')  # cartella corrente


def is_already_converted(match: dict) -> bool:
    """Controlla se il file è già nel formato target."""
    return 'DateUtc' in match and 'HomeTeamScore' in match


def convert_match(match: dict) -> dict:
    return {
        'DateUtc': match.get('Date', ''),
        'HomeTeam': match.get('HomeTeam', ''),
        'AwayTeam': match.get('AwayTeam', ''),
        'HomeTeamScore': match.get('FTHG', None),
        'AwayTeamScore': match.get('FTAG', None),
    }


def convert_file(file_path: Path):
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list) or len(data) == 0:
            print(f"⛔ Skippato (formato non valido): {file_path.name}")
            return

        # Se è già convertito → skip
        if is_already_converted(data[0]):
            print(f"↪️ Già convertito: {file_path.name}")
            return

        converted = [convert_match(match) for match in data]

        # 🔥 Sovrascrittura
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(converted, f, ensure_ascii=False, indent=2)

        print(f"✅ Sovrascritto: {file_path.name}")

    except Exception as e:
        print(f"❌ Errore su {file_path.name}: {e}")


def main():
    json_files = list(INPUT_DIR.glob('*.json'))

    if not json_files:
        print("⚠️ Nessun file JSON trovato.")
        return

    for file in json_files:
        convert_file(file)


if __name__ == '__main__':
    main()