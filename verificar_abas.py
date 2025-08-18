#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar as abas da planilha gerada
"""

import pandas as pd
import os

def verificar_abas():
    arquivo = "VR_MENSAL_GERADO.xlsx"
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo {arquivo} não encontrado!")
        return
    
    try:
        # Verificar todas as abas
        xl_file = pd.ExcelFile(arquivo)
        print(f"📋 Abas encontradas em {arquivo}:")
        for i, sheet in enumerate(xl_file.sheet_names, 1):
            print(f"  {i}. {sheet}")
        
        # Tentar carregar a primeira aba
        if xl_file.sheet_names:
            primeira_aba = xl_file.sheet_names[0]
            print(f"\n📊 Carregando primeira aba: '{primeira_aba}'")
            df = pd.read_excel(arquivo, sheet_name=primeira_aba)
            print(f"   Dimensões: {df.shape}")
            print(f"   Colunas: {list(df.columns)}")
            
            if len(df) > 0:
                print(f"\n📋 Primeiras 3 linhas:")
                print(df.head(3).to_string())
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    verificar_abas()