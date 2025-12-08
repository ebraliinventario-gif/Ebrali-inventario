import os
from pathlib import Path
from typing import Iterable, List, Sequence

import gspread
from dotenv import dotenv_values, load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
DOTENV_PATH = BASE_DIR / ".env"
DEFAULT_ENV = {
    # Caminho padrão para o JSON de credenciais do serviço do Google
    "GOOGLE_APPLICATION_CREDENTIALS": "./minha-app-node-sheets-abc123.json",
    # ID fixo da planilha informada na URL
    # https://docs.google.com/spreadsheets/d/1cn-9mg-_8QzYtZpCoLpDvglA036m1j70OvQaO3Ebo4M/edit?gid=0#gid=0
    "SPREADSHEET_ID": "1cn-9mg-_8QzYtZpCoLpDvglA036m1j70OvQaO3Ebo4M",
    # Nome da aba padrão criada pelo Google para a guia principal
    "WORKSHEET_TITLE": "Sheet1",
}

if DOTENV_PATH.exists():
    load_dotenv(str(DOTENV_PATH), override=False)
    for chave, valor in dotenv_values(str(DOTENV_PATH)).items():
        if valor is not None and not os.getenv(chave):
            os.environ[chave] = valor
else:
    print(f"[Aviso] Arquivo .env não encontrado em {DOTENV_PATH}. Usando valores padrão.")

for chave, valor in DEFAULT_ENV.items():
    if not os.getenv(chave):
        os.environ[chave] = valor

HEADERS = [
    "Código Endereço",
    "Descrição Endereço",
    "Armazém",
    "Cód. Produto",
    "Descrição Produto",
    "Qtde",
    "Lote",
    "Validade",
    "Conferente",
]

def _get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variável de ambiente '{name}' não encontrada. Verifique o arquivo .env.")
    return value


credentials_path = _get_env("GOOGLE_APPLICATION_CREDENTIALS")
spreadsheet_id = _get_env("SPREADSHEET_ID")
worksheet_title = _get_env("WORKSHEET_TITLE")

credentials_full_path = Path(credentials_path)
if not credentials_full_path.is_absolute():
    credentials_full_path = (BASE_DIR / credentials_full_path).resolve()

client = gspread.service_account(filename=str(credentials_full_path))
sheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_title)


def _get_sheet_by_title(title: str):
    try:
        return client.open_by_key(spreadsheet_id).worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        raise RuntimeError(f"Worksheet '{title}' não encontrada na planilha") from None


def _normalize_row(valores: Sequence[object]) -> List[str]:
    lista = list(valores)
    padded = (lista + [""] * len(HEADERS))[: len(HEADERS)]
    return ["" if valor is None else str(valor) for valor in padded]


def salvar(*valores):
    linha = _normalize_row(valores)
    sheet.append_row(linha, value_input_option="USER_ENTERED")
    print("Gravado →", linha)


def salvar_linhas(
    linhas: Iterable[Sequence[object]],
    *,
    incluir_header: bool = True,
    limpar_antes: bool = True,
    worksheet_title: str | None = None,
    conflict_policy: str = "merge",
):
    registros = [_normalize_row(linha) for linha in linhas]
    destino = sheet if worksheet_title is None else _get_sheet_by_title(worksheet_title)

    if not registros:
        return {"added": 0, "updated": 0, "conflicts": []}

    # If requested, clear and simply append everything (fresh export)
    if limpar_antes:
        destino.clear()
        payload: List[List[str]] = []
        if incluir_header:
            payload.append(HEADERS)
        payload.extend(registros)
        if payload:
            destino.append_rows(payload, value_input_option="USER_ENTERED")
        print(f"Gravadas {len(registros)} linhas no Google Sheets (limpou antes)")
        return {"added": len(registros), "updated": 0, "conflicts": []}

    # When not clearing, we try to merge into existing rows without overwriting
    existing = destino.get_all_values()

    # Detect header row
    data_start_index = 0
    header_present = False
    if existing and existing[0] == HEADERS:
        header_present = True
        data_start_index = 1

    code_to_row = {}
    for i, row in enumerate(existing[data_start_index:], start=data_start_index + 1):
        if not row:
            continue
        codigo = row[0] if len(row) > 0 else ""
        code_to_row[str(codigo).strip()] = (i, [str(v) for v in row] + [""] * max(0, len(HEADERS) - len(row)))

    to_append: List[List[str]] = []
    updated = 0
    conflicts: List[dict] = []

    for registro in registros:
        codigo = registro[0].strip()
        if codigo == "":
            # no code, treat as new row
            to_append.append(registro)
            continue

        if codigo in code_to_row:
            row_idx, existing_row = code_to_row[codigo]
            # normalize existing row length
            existing_row = (existing_row + [""] * len(HEADERS))[: len(HEADERS)]
            new_row = existing_row.copy()
            changed = False
            for col_idx in range(len(HEADERS)):
                incoming = registro[col_idx] if col_idx < len(registro) else ""
                existing_val = existing_row[col_idx]
                if incoming and not existing_val:
                    # fill empty cell
                    new_row[col_idx] = incoming
                    changed = True
                elif incoming and existing_val and incoming != existing_val:
                    # attempted overwrite -> record conflict (do not overwrite)
                    conflicts.append({"codigo": codigo, "column": HEADERS[col_idx], "existing": existing_val, "incoming": incoming})
            if changed:
                # write back the merged row
                # gspread row numbers are 1-based
                start_col = "A"
                end_col = chr(ord("A") + len(HEADERS) - 1)
                range_str = f"{start_col}{row_idx}:{end_col}{row_idx}"
                destino.update(range_str, [new_row])
                updated += 1
        else:
            to_append.append(registro)

    if to_append:
        # If caller requested header and sheet has no header, insert it first
        if incluir_header and not header_present:
            destino.append_row(HEADERS, value_input_option="USER_ENTERED")
        destino.append_rows(to_append, value_input_option="USER_ENTERED")

    added = len(to_append)
    print(f"Adicionadas {added} linhas e atualizadas {updated} linhas no Google Sheets")
    return {"added": added, "updated": updated, "conflicts": conflicts}


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        salvar(*sys.argv[1:])
    else:
        print("Uso: python scripts/salvar.py 001 Camisa P 10 02/12/2025 João")
