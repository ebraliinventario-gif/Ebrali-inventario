#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para processar a lista completa de produtos fornecida pelo usuário.
Formato: PRODUTO EMBALAGEM	CÓDIGO
"""

import re

def processar_linha(linha):
    """Processa uma linha no formato: PRODUTO EMBALAGEM	CÓDIGO"""
    linha = linha.strip()
    if not linha or '\t' not in linha:
        return None
    
    partes = linha.split('\t')
    if len(partes) < 2:
        return None
    
    produto_embalagem = partes[0].strip()
    codigo = partes[1].strip()
    
    # Extrair produto e embalagem
    # Padrão: número seguido de KG ou UNIDADE no final
    match = re.match(r'^(.+?)\s+(\d+[,\d]*\.?\d*\s*KG|UNIDADE)$', produto_embalagem, re.IGNORECASE)
    if match:
        produto = match.group(1).strip()
        embalagem = match.group(2).strip().upper()
    else:
        # Tentar encontrar padrão KG no final
        match_kg = re.search(r'\s+(\d+[,\d]*\.?\d*\s*KG|UNIDADE)$', produto_embalagem, re.IGNORECASE)
        if match_kg:
            produto = produto_embalagem[:match_kg.start()].strip()
            embalagem = match_kg.group(1).strip().upper()
        else:
            produto = produto_embalagem
            embalagem = ''
    
    return {
        'codigo': codigo.strip(),
        'produto': produto,
        'embalagem': embalagem
    }


def processar_lista_completa(texto):
    """Processa toda a lista de produtos"""
    produtos_dict = {}
    
    linhas = texto.split('\n')
    print(f"Total de linhas no arquivo: {len(linhas)}")
    
    linhas_processadas = 0
    linhas_ignoradas = 0
    
    for linha in linhas:
        resultado = processar_linha(linha)
        if resultado:
            produtos_dict[resultado['codigo']] = {
                'produto': resultado['produto'],
                'embalagem': resultado['embalagem']
            }
            linhas_processadas += 1
        else:
            linhas_ignoradas += 1
    
    print(f"Linhas processadas: {linhas_processadas}")
    print(f"Linhas ignoradas: {linhas_ignoradas}")
    
    return produtos_dict


def gerar_javascript(produtos_dict):
    """Gera o código JavaScript do objeto PRODUTOS."""
    linhas = ['        const PRODUTOS = {']
    
    
    def ordenar_codigo(codigo):
        
        match = re.match(r'^(\d+)([A-ZN]*)$', codigo.upper())
        if match:
            num = int(match.group(1)) if match.group(1) else 0
            letra = match.group(2) or ''
            return (num, letra)
        return (999999, codigo)
    
    codigos_ordenados = sorted(produtos_dict.keys(), key=ordenar_codigo)
    
    for i, codigo in enumerate(codigos_ordenados):
        produto = produtos_dict[codigo]
        produto_str = produto['produto'].replace("'", "\\'").replace('"', '\\"')
        embalagem_str = produto['embalagem'].replace("'", "\\'").replace('"', '\\"')
        
        linha = f"            '{codigo}': {{ produto: '{produto_str}', embalagem: '{embalagem_str}' }}"
        
        if i < len(codigos_ordenados) - 1:
            linha += ','
        
        linhas.append(linha)
    
    linhas.append('        };')
    
    return '\n'.join(linhas)


def atualizar_index_html(arquivo_lista='lista_produtos_completa.txt'):
    """Atualiza o arquivo index.html com o objeto PRODUTOS completo."""
    try:
        # Ler todas as linhas, incluindo vazias
        with open(arquivo_lista, 'r', encoding='utf-8', newline='') as f:
            linhas = f.readlines()
        texto = ''.join(linhas)
    except FileNotFoundError:
        print(f"❌ Arquivo {arquivo_lista} não encontrado!")
        print("Por favor, crie o arquivo com toda a lista de produtos.")
        return
    
    produtos_dict = processar_lista_completa(texto)
    js_code = gerar_javascript(produtos_dict)
    
    # Ler o arquivo index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Encontrar e substituir o objeto PRODUTOS
    padrao = r'const PRODUTOS = \{.*?\n        \};'
    novo_conteudo = re.sub(padrao, js_code, conteudo, flags=re.DOTALL)
    
    # Salvar o arquivo atualizado
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(novo_conteudo)
    
    print(f"✅ Objeto PRODUTOS atualizado com {len(produtos_dict)} produtos!")
    print(f"📝 Código gerado e inserido no index.html")


if __name__ == '__main__':
    import sys
    arquivo = sys.argv[1] if len(sys.argv) > 1 else 'lista_produtos_completa.txt'
    atualizar_index_html(arquivo)

