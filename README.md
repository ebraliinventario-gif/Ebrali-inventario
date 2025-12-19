<div align="center">
  <img src="logo_ebrali-2025.png" alt="Ebrali" width="120" />

  # Controle de Inventário

  Interface web para conferência de endereços/produtos e **exportação em lote** para **Google Sheets**.

  [![Frontend](https://img.shields.io/badge/frontend-HTML%20%2B%20CSS%20%2B%20JS-14532D)](#)
  [![Backend](https://img.shields.io/badge/backend-Python-3776AB)](#)
  [![API](https://img.shields.io/badge/API-%2Fapi%2Fexport-111827)](#api)
  [![PWA](https://img.shields.io/badge/PWA-service%20worker-0ea5e9)](#pwa)
</div>

## Visão geral

Ao clicar em **Exportar Excel** na interface (`index.html`), os registros preenchidos são enviados para um backend em Python, que grava os dados no **Google Sheets** via `gspread`.

Planilha (exemplo do projeto):

`https://docs.google.com/spreadsheets/d/1cn-9mg-_8QzYtZpCoLpDvglA036m1j70OvQaO3Ebo4M/edit`

## Sumário

- [Recursos](#recursos)
- [Arquitetura](#arquitetura)
- [Quickstart (local)](#quickstart-local)
- [Configuração (.env)](#configuração-env)
- [API](#api)
- [PWA](#pwa)
- [Troubleshooting](#troubleshooting)
- [Segurança](#segurança)

## Recursos

- **Tabela de inventário** com filtros e edição rápida.
- **Identificação de conferente** (salva no navegador).
- **Exportação em lote** com status e proteção contra cliques repetidos (cooldown).
- **PWA offline** (cache via Service Worker) para abrir mais rápido e funcionar mesmo com rede instável.

## Arquitetura

- **Frontend**
  - `index.html`: UI + lógica (JS inline)
  - `styles.css`: tema e layout
  - `dados_ruas*.js`: dados iniciais de endereços
  - `sw.js`: cache/PWA

- **Backend (Python)**
  - Opção 1: `server.py` (Flask) — expõe `POST /api/export`
  - Opção 2: `backend/main.py` (FastAPI) — expõe `POST /api/export`
  - `scripts/salvar.py`: integração com Google Sheets (`gspread`)

## Quickstart (local)

### Pré-requisitos

- Python 3.10+

### Instalação

```bash
pip install -r requirements.txt
```

Ou (se preferir instalar manualmente):

```bash
pip install gspread python-dotenv flask fastapi uvicorn google-auth
```

### Rodando o backend

Escolha uma das opções:

**Flask**

```bash
python server.py
```

**FastAPI**

```bash
python backend/main.py
```

### Rodando o frontend

- Abra `index.html` no navegador, ou sirva com uma extensão como “Live Server”.

## Configuração (.env)

Crie um arquivo `.env` na raiz do projeto com:

```
GOOGLE_APPLICATION_CREDENTIALS=./minha-app-node-sheets-abc123.json
SPREADSHEET_ID=1cn-9mg-_8QzYtZpCoLpDvglA036m1j70OvQaO3Ebo4M
WORKSHEET_TITLE=Planilha1
```

Depois, **compartilhe a planilha** com o e-mail do *service account* contido no JSON de credenciais.

Obs: `.env` e credenciais `.json` já devem ficar fora do Git (ver `.gitignore`).

## API

### `POST /api/export`

O frontend envia um payload no formato:

```json
{
  "records": [
    {
      "codigo": "PI01A0101",
      "descricao": "...",
      "armazem": "01",
      "custom1": "Cód. Produto",
      "custom2": "Descrição Produto",
      "custom3": "Qtde",
      "lote": "...",
      "validade": "...",
      "conferente": "..."
    }
  ],
  "clearBefore": false,
  "includeHeader": true,
  "destinoPlanilha": "Planilha1"
}
```

## PWA

- O `sw.js` faz cache dos arquivos principais.
- Para atualizar o app em aparelhos já instalados, publique uma nova versão e recarregue (o Service Worker pode manter cache até a próxima atualização).

## Troubleshooting

- **Erro 429 / Quota do Google Sheets**
  - Espere alguns segundos e tente novamente.
  - Evite múltiplos dispositivos exportando ao mesmo tempo.

- **Servidor ocupado (503)**
  - Significa que já existe outra exportação em andamento.

- **Credenciais inválidas / planilha não encontrada**
  - Confira `GOOGLE_APPLICATION_CREDENTIALS` e `SPREADSHEET_ID`.
  - Garanta que a planilha foi compartilhada com o service account.

## Segurança

- Não faça commit de `.env` ou credenciais JSON.
- Se houver vazamento, revogue a chave no Google Cloud imediatamente.

## Dica para deixar ainda mais bonito

- Adicione prints na pasta do projeto e referencie aqui:
  - `./docs/screenshot-1.png`
  - `./docs/screenshot-2.png`

E inclua uma seção “Screenshots” com imagens.
