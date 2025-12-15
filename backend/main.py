from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from threading import Lock
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.salvar import HEADERS, salvar_linhas  # noqa: E402

EXPORT_LOCK = Lock()

PLANILHA_ALIASES = {
    "planilha1": "Planilha1",
    "planilha 1": "Planilha1",
    "contagem 01": "Planilha1",
    "contagem01": "Planilha1",
    "planilha2": "Planilha2",
    "planilha 2": "Planilha2",
    "contagem 02": "Planilha2",
    "contagem02": "Planilha2",
}


def _resolver_destino_planilha(valor: Optional[str]) -> Optional[str]:
    if not valor:
        return None
    chave = valor.strip().lower()
    return PLANILHA_ALIASES.get(chave, valor)


class Record(BaseModel):
    codigo: str = ""
    descricao: str = ""
    armazem: str = ""
    custom1: str = ""
    custom2: str = ""
    custom3: str = ""
    lote: str = ""
    validade: str = ""
    conferente: str = ""


class ExportPayload(BaseModel):
    records: List[Record]
    clearBefore: bool = False
    includeHeader: bool = True
    destinoPlanilha: Optional[str] = None
    conflictPolicy: Optional[str] = "merge"


app = FastAPI(title="Inventário Ebrali API")

DEFAULT_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://seuusuario.github.io",
    "https://seuusuario.github.io/nome-do-repo",
    "https://ebrali-inventario.onrender.com",
]

env_allowed = os.getenv("ALLOWED_ORIGINS")
if env_allowed:
    allowed_origins = [
        origin.strip()
        for origin in env_allowed.split(",")
        if origin.strip()
    ]
else:
    allowed_origins = DEFAULT_ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _record_to_row(record: Record) -> list[str]:
    dados = record.dict()
    return [
        dados.get("codigo", ""),
        dados.get("descricao", ""),
        dados.get("armazem", ""),
        dados.get("custom1", ""),
        dados.get("custom2", ""),
        dados.get("custom3", ""),
        dados.get("lote", ""),
        dados.get("validade", ""),
        dados.get("conferente", ""),
    ]


@app.get("/")
def read_root():
    return {"message": "Backend no Render rodando!"}


@app.get("/api/hello")
def hello():
    return {"texto": "Olá do Python no Render!"}


@app.post("/api/export")
def api_export(payload: ExportPayload):
    if not payload.records:
        return {"status": "sem dados"}

    linhas = [_record_to_row(record) for record in payload.records]
    destino_planilha = _resolver_destino_planilha(payload.destinoPlanilha)

    queue_started = time.perf_counter()
    lock_wait_ms = 0
    processing_ms = 0

    acquired = EXPORT_LOCK.acquire(timeout=30)
    if not acquired:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Servidor ocupado",
                "details": "Há outro envio em processamento. Tente novamente em instantes.",
            },
        )

    try:
        lock_wait_ms = int((time.perf_counter() - queue_started) * 1000)
        processing_started = time.perf_counter()
        result = salvar_linhas(
            linhas,
            incluir_header=payload.includeHeader,
            limpar_antes=payload.clearBefore,
            worksheet_title=destino_planilha,
            conflict_policy=payload.conflictPolicy or "merge",
        )
        processing_ms = int((time.perf_counter() - processing_started) * 1000)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Falha ao salvar dados no Google Sheets",
                "details": str(exc),
                "timings": {"lockWaitMs": lock_wait_ms, "processingMs": processing_ms},
            },
        ) from exc
    finally:
        EXPORT_LOCK.release()

    timings = {"lockWaitMs": lock_wait_ms, "processingMs": processing_ms}
    if isinstance(result, dict):
        return {"status": "ok", "report": result, "columns": HEADERS, "timings": timings}
    return {"status": "ok", "rows": len(linhas), "columns": HEADERS, "timings": timings}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
