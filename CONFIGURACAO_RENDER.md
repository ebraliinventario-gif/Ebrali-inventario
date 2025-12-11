# 🚀 Guia Completo de Configuração no Render

## 📋 Configurações Necessárias no Render Dashboard

### 1. **Build Command**
```
pip install -r requirements.txt
```

### 2. **Start Command**
```
gunicorn -w 4 -b 0.0.0.0:$PORT server:app
```

### 3. **Health Check Path**
```
/healthz
```

### 4. **Root Directory**
Deixe em branco (vazio)

---

## 🔐 Environment Variables (Variáveis de Ambiente)

Configure estas variáveis no dashboard do Render:

| Name (Key) | Value |
|------------|-------|
| `GOOGLE_APPLICATION_CREDENTIALS` | `/etc/secrets/minha-app-node-sheets-a27f04d71760.json` |
| `SPREADSHEET_ID` | `1cn-9mg-_8QzYtZpCoLpDvglA036m1j70OvQaO3Ebo4M` |
| `WORKSHEET_TITLE` | `Planilha1` |
| `FLASK_ENV` | `production` |
| `PYTHON_VERSION` | `3.11.7` |

**⚠️ IMPORTANTE:**
- `GOOGLE_APPLICATION_CREDENTIALS` deve apontar para o caminho do Secret File
- O nome do arquivo no Secret File deve ser exatamente `minha-app-node-sheets-a27f04d71760.json`

---

## 📁 Secret Files

### Configuração do Secret File:

1. Vá em **Advanced** → **Secret Files**
2. Clique em **+ Add Secret File**
3. **Filename**: `minha-app-node-sheets-a27f04d71760.json`
4. **Content**: Cole o conteúdo completo do arquivo JSON do service account
   - Abra o arquivo `minha-app-node-sheets-a27f04d71760.json` localmente
   - Copie TODO o conteúdo (todo o JSON)
   - Cole no campo Content do Secret File

**⚠️ NUNCA faça commit do arquivo JSON no GitHub!**

---

## ✅ Checklist de Configuração

- [ ] Build Command configurado: `pip install -r requirements.txt`
- [ ] Start Command configurado: `gunicorn -w 4 -b 0.0.0.0:$PORT server:app`
- [ ] Health Check Path configurado: `/healthz`
- [ ] Root Directory está vazio
- [ ] Secret File criado com o nome correto
- [ ] Secret File contém o JSON completo do service account
- [ ] Variável `GOOGLE_APPLICATION_CREDENTIALS` aponta para `/etc/secrets/minha-app-node-sheets-a27f04d71760.json`
- [ ] Variável `SPREADSHEET_ID` configurada
- [ ] Variável `WORKSHEET_TITLE` configurada como `Planilha1`
- [ ] Variável `FLASK_ENV` configurada como `production`
- [ ] Service account tem acesso à planilha do Google Sheets

---

## 🔍 Verificação do Service Account

Certifique-se de que:

1. O service account (`sheets-access@minha-app-node-sheets.iam.gserviceaccount.com`) tem acesso à planilha
2. Para dar acesso:
   - Abra a planilha no Google Sheets
   - Clique em **Compartilhar**
   - Adicione o email: `sheets-access@minha-app-node-sheets.iam.gserviceaccount.com`
   - Dê permissão de **Editor**

---

## 🐛 Troubleshooting

### Erro: "invalid_scope"
- ✅ **Corrigido**: O código agora usa escopos explícitos

### Erro: "File not found"
- Verifique se o Secret File foi criado com o nome exato
- Verifique se `GOOGLE_APPLICATION_CREDENTIALS` aponta para `/etc/secrets/nome-do-arquivo.json`

### Erro: "Worksheet not found"
- Verifique se a aba `Planilha1` existe na planilha
- Ou altere `WORKSHEET_TITLE` para o nome correto da aba

### Health check falhando
- Verifique se o endpoint `/healthz` está respondendo
- O servidor precisa estar rodando para o health check funcionar

---

## 📝 Comandos Git para Subir as Alterações

```bash
# Adicionar arquivos modificados
git add scripts/salvar.py render.yaml

# Fazer commit
git commit -m "Configurar aplicação para Render com inicialização lazy do Google Sheets"

# Fazer push
git push origin main
```

**⚠️ NÃO faça commit do arquivo JSON:**
```bash
# Se o JSON estiver no repositório, remova:
git rm minha-app-node-sheets-a27f04d71760.json
git commit -m "Remover credenciais do repositório"
git push origin main
```

---

## 🎯 Após o Deploy

1. Acesse a URL do serviço (ex: `https://ebrali-inventario-24ra.onrender.com`)
2. Teste o endpoint de health: `https://ebrali-inventario-24ra.onrender.com/healthz`
3. Deve retornar: `{"status": "ok"}`
4. Teste a API: `POST https://ebrali-inventario-24ra.onrender.com/api/export`

---

## 📞 Suporte

Se ainda houver problemas:
1. Verifique os logs no Render Dashboard → Logs
2. Verifique se todas as variáveis de ambiente estão configuradas
3. Verifique se o Secret File foi criado corretamente



