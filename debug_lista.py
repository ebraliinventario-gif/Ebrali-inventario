#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de debug para verificar o processamento da lista"""

import re

def processar_linha(linha):
    """Processa uma linha no formato: PRODUTO EMBALAGEM	CÓDIGO"""
    linha = linha.strip()
    if not linha:
        return None
    
    if '\t' not in linha:
        print(f"Linha sem tab: {linha[:50]}")
        return None
    
    partes = linha.split('\t')
    if len(partes) < 2:
        print(f"Linha com menos de 2 partes: {linha[:50]}")
        return None
    
    produto_embalagem = partes[0].strip()
    codigo = partes[1].strip()
    
    # Extrair produto e embalagem
    match = re.match(r'^(.+?)\s+(\d+[,\d]*\.?\d*\s*KG|UNIDADE)$', produto_embalagem, re.IGNORECASE)
    if match:
        produto = match.group(1).strip()
        embalagem = match.group(2).strip().upper()
    else:
        match_kg = re.search(r'\s+(\d+[,\d]*\.?\d*\s*KG|UNIDADE)$', produto_embalagem, re.IGNORECASE)
        if match_kg:
            produto = produto_embalagem[:match_kg.start()].strip()
            embalagem = match_kg.group(1).strip().upper()
        else:
            print(f"Não conseguiu separar produto/embalagem: {produto_embalagem[:50]}")
            produto = produto_embalagem
            embalagem = ''
    
    return {
        'codigo': codigo.strip(),
        'produto': produto,
        'embalagem': embalagem
    }

# Ler arquivo
with open('lista_produtos_completa.txt', 'r', encoding='utf-8') as f:
    linhas = f.readlines()

print(f"Total de linhas no arquivo: {len(linhas)}")

produtos_dict = {}
linhas_processadas = 0
linhas_ignoradas = 0

for i, linha in enumerate(linhas, 1):
    resultado = processar_linha(linha)
    if resultado:
        produtos_dict[resultado['codigo']] = {
            'produto': resultado['produto'],
            'embalagem': resultado['embalagem']
        }
        linhas_processadas += 1
    else:
        linhas_ignoradas += 1
        if linhas_ignoradas <= 10:  # Mostrar apenas as primeiras 10 linhas ignoradas
            print(f"Linha {i} ignorada: {linha[:80]}")

print(f"\n✅ Linhas processadas: {linhas_processadas}")
print(f"❌ Linhas ignoradas: {linhas_ignoradas}")
print(f"📦 Produtos únicos: {len(produtos_dict)}")







