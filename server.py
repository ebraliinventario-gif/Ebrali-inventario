import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

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


def _resolver_destino_planilha(valor: str | None) -> str | None:
    if not valor:
        return None
    chave = valor.strip().lower()
    return PLANILHA_ALIASES.get(chave, valor)

from flask import Flask, jsonify, request, send_from_directory

from scripts.salvar import HEADERS, salvar_linhas

# Configurar pasta de arquivos estáticos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

# Servir arquivos estáticos
@app.route('/')
def serve_index():
    """Serve o arquivo index.html"""
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve arquivos estáticos (CSS, JS, etc)"""
    if filename.endswith(('.html', '.css', '.js', '.json')):
        filepath = os.path.join(BASE_DIR, filename)
        if os.path.exists(filepath):
            return send_from_directory(BASE_DIR, filename)
    return {"error": "Not found"}, 404


def _record_to_row(record):
    """Converte um dicionário vindo do front em uma linha para a planilha."""
    return [
        record.get("codigo", ""),
        record.get("descricao", ""),
        record.get("armazem", ""),
        record.get("custom1", ""),
        record.get("custom2", ""),
        record.get("custom3", ""),
        record.get("lote", ""),
        record.get("validade", ""),
        record.get("conferente", ""),
    ]


@app.after_request
def add_cors_headers(response):
    """
    Libera o acesso CORS para o front abrir o HTML localmente ou em outro host.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.route("/api/export", methods=["OPTIONS"])
def api_export_options():
    """Pré‑voo CORS (OPTIONS) para o endpoint de exportação."""
    return ("", 204)


@app.route('/healthz', methods=['GET'])
def healthz():
    """Health check endpoint used by Render and other platforms.

    Returns HTTP 200 when the app is up. Keep this lightweight.
    """
    return jsonify({"status": "ok"}), 200


@app.post("/api/export")
def api_export():
    try:
        payload = request.get_json(force=True, silent=False)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"JSON inválido: {exc}"}), 400

    if not isinstance(payload, dict):
        return jsonify({"error": "Envie um objeto JSON"}), 400

    records = payload.get("records")
    if not isinstance(records, list):
        return jsonify({"error": "'records' precisa ser uma lista"}), 400

    linhas = []
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            return jsonify({"error": f"Registro #{idx + 1} inválido"}), 400
        linhas.append(_record_to_row(record))

    if not linhas:
        return jsonify({"status": "sem dados"})

    limpar = bool(payload.get("clearBefore", False))
    incluir_header = bool(payload.get("includeHeader", True))
    destino_planilha = _resolver_destino_planilha(payload.get("destinoPlanilha"))

    try:
        result = salvar_linhas(
            linhas,
            incluir_header=incluir_header,
            limpar_antes=limpar,
            worksheet_title=destino_planilha,
            conflict_policy=payload.get("conflictPolicy", "merge"),
        )
    except Exception as exc:  # noqa: BLE001
        # Retorna erro amigável ao front em caso de falha ao falar com o Google
        return (
            jsonify(
                {
                    "error": "Falha ao salvar dados no Google Sheets",
                    "details": str(exc),
                }
            ),
            500,
        )

    # retornamos relatório detalhado do que foi adicionado/atualizado
    if isinstance(result, dict):
        return jsonify({"status": "ok", "report": result, "columns": HEADERS})
    return jsonify({"status": "ok", "rows": len(linhas), "columns": HEADERS})


if __name__ == "__main__":
    # host='0.0.0.0' permite acesso também a partir de outros dispositivos na rede,
    # se necessário. Ajuste a porta aqui se quiser mudar a URL do front.
    port = int(os.getenv('PORT', 3000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host="0.0.0.0", port=port, debug=debug)
