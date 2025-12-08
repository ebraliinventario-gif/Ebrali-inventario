# Ebrali Inventário - Deploy Guide

## Deploy no Render

### Pré-requisitos
1. Conta no [Render](https://render.com)
2. Repositório no GitHub com o código
3. Arquivo de credenciais do Google Sheets

### Passo 1: Preparar o Repositório

Todos os arquivos necessários já estão configurados:
- `Procfile` - Define como rodar a aplicação
- `requirements.txt` - Dependências Python
- `render.yaml` - Configuração opcional

### Passo 2: Fazer Push para GitHub

```bash
cd c:\Users\pcp\Desktop\Ebrali_inventario-main
git add .
git commit -m "Preparar para deploy no Render"
git push origin main
```

### Passo 3: Deploy no Render

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório GitHub (`Ebrali-inventario`)
4. Preencha os campos:
   - **Name**: `ebrali-inventario`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT server:app`
   - **Plan**: Free (ou pago se preferir)

### Passo 4: Configurar Variáveis de Ambiente

No dashboard do Render, vá para "Environment":

1. Clique em "Add Environment Variable"
2. Adicione:
   - **Key**: `GOOGLE_SHEETS_CREDENTIALS_JSON`
   - **Value**: Cole todo o conteúdo do arquivo JSON de credenciais do Google

### Passo 5: Deploy Automático

- O Render fará deploy automático sempre que você fizer `push` para `main`
- Veja o progresso em "Logs"

## URLs

- **Frontend**: `https://seu-nome.onrender.com` (servirá o `index.html`)
- **Backend API**: `https://seu-nome.onrender.com/api/export`

## Variáveis de Ambiente Necessárias

Crie um arquivo `.env.example` (já criado) e configure:

```env
GOOGLE_SHEETS_CREDENTIALS_JSON=seu_json_aqui
FLASK_ENV=production
PORT=3000
```

## Troubleshooting

### A aplicação não inicia
- Verifique os logs no Render: `Logs` → `Build` e `Runtime Logs`
- Certifique-se de que todas as dependências estão em `requirements.txt`

### Erro de CORS
- O servidor já está configurado para aceitar requisições de qualquer origem
- Verifique se o `Access-Control-Allow-Origin` está configurado

### Credenciais do Google Sheets não funcionam
- Verifique se `GOOGLE_SHEETS_CREDENTIALS_JSON` está configurado corretamente
- Certifique-se de que o JSON é válido (sem quebras de linha extras)

## Estrutura do Projeto

```
├── server.py              # Servidor Flask
├── index.html             # Frontend
├── styles.css             # Estilos
├── Procfile               # Configuração para Render
├── requirements.txt       # Dependências Python
├── render.yaml            # Configuração alternativa (opcional)
├── .env.example           # Template de variáveis de ambiente
└── backend/
    ├── main.py            # Alternativa com FastAPI
    └── requirements.txt
```

## Desenvolvimiento Local

Para testar antes de fazer deploy:

```bash
pip install -r requirements.txt
python server.py
```

Depois acesse `http://localhost:3000`
