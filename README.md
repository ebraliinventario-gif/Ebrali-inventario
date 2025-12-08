# Controle de Inventário — Exportação automática para Google Sheets

Ao clicar em **Exportar Excel** na interface (`index.html`), todos os registros carregados/alterados são enviados para a planilha do Google Sheets `https://docs.google.com/spreadsheets/d/1cn-9mg-_8QzYtZpCoLpDvglA036m1j70OvQaO3Ebo4M/edit`. O backend exposto em `server.py` recebe os dados e usa `gspread` para gravá-los.

## Pré-requisitos

1. Python 3.10+
2. Dependências (uma vez):
   ```bash
   pip install gspread python-dotenv flask
   ```
3. Compartilhe a planilha com o e-mail do service account listado em `minha-app-node-sheets-abc123.json`.

## Configuração do ambiente

O arquivo `.env` deve conter:

```
GOOGLE_APPLICATION_CREDENTIALS=./minha-app-node-sheets-abc123.json
SPREADSHEET_ID=1cn-9mg-_8QzYtZpCoLpDvglA036m1j70OvQaO3Ebo4M
WORKSHEET_TITLE=Planilha1
```

O `.env`, arquivos `.json` de credenciais e `__pycache__` já estão ignorados no `.gitignore`.

## Estrutura Python

- `scripts/salvar.py`: abstrai a escrita na planilha (funções `salvar` e `salvar_linhas`).
- `server.py`: expõe `POST /api/export`, validando o payload e enviando todas as linhas em lote para o Google Sheets.

## Execução

1. Certifique-se de que o arquivo de credenciais está na raiz do projeto.
2. Carregue as variáveis de ambiente (`.env`).
3. Inicie o backend:
   ```bash
   python server.py
   ```
4. Abra `index.html` no navegador (ou sirva via Live Server). Quando clicar em **Exportar Excel**, o frontend envia `records` para `http://localhost:3000/api/export`; o servidor limpa a planilha e grava os dados com cabeçalho.

## Testes rápidos

- **Manual**: rode `python scripts/salvar.py 001 "Camisa P" 10 "02/12/2025" "João"` para verificar se a linha aparece na planilha.
- **API**: com o servidor rodando, faça `curl -X POST http://localhost:3000/api/export -H "Content-Type: application/json" -d '{"records":[{"codigo":"PI01A0101"}]}'`.

## Segurança

- Não faça commit do `.env` ou das credenciais JSON.
- Revogue a chave no console do Google Cloud se houver vazamento.
